import random
import pytweening

from selenium.common import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains

from cursors.utilities.human_curve_generator import HumanizeMouseTrajectory


class WebAdjuster:
    def __init__(self, driver):
        self.__driver = driver
        self.__action = ActionChains(self.__driver, duration=0)
        self.origin_coordinate = [0, 0]

    def move_to(
        self,
        element_or_pos,
        origin_coordinates=None,
        absolute_offset=False,
        relative_position=None,
        human_curve=None,
    ):
        """Moves the cursors, trying to mimic human behaviour!"""
        origin = origin_coordinates
        if origin_coordinates is None:
            origin = self.origin_coordinate

        pre_origin = tuple(origin)
        if isinstance(element_or_pos, list):
            if not absolute_offset:
                x, y = element_or_pos[0], element_or_pos[1]
            else:
                x, y = (
                    element_or_pos[0] + pre_origin[0],
                    element_or_pos[1] + pre_origin[1],
                )
        else:
            script = "return { x: Math.round(arguments[0].getBoundingClientRect().left), y: Math.round(arguments[0].getBoundingClientRect().top) };"
            destination = self.__driver.execute_script(script, element_or_pos)
            if relative_position is None:
                x_random_off = random.choice(range(20, 80)) / 100
                y_random_off = random.choice(range(20, 80)) / 100

                x, y = destination["x"] + (
                    element_or_pos.size["width"] * x_random_off
                ), destination["y"] + (element_or_pos.size["height"] * y_random_off)
            else:
                abs_exact_offset = self.calculate_absolute_offset(
                    element_or_pos, relative_position
                )
                x_exact_off, y_exact_off = abs_exact_offset[0], abs_exact_offset[1]
                x, y = destination["x"] + x_exact_off, destination["y"] + y_exact_off

        (
            offset_boundary_x,
            offset_boundary_y,
            knots_count,
            distortion_mean,
            distortion_st_dev,
            distortion_frequency,
            tween,
            target_points,
        ) = self.generate_random_curve_parameters(
            self.__driver, [origin[0], origin[1]], [x, y]
        )

        if not human_curve:
            human_curve = HumanizeMouseTrajectory(
                [origin[0], origin[1]],
                [x, y],
                offset_boundary_x=offset_boundary_x,
                offset_boundary_y=offset_boundary_y,
                knots_count=knots_count,
                distortion_mean=distortion_mean,
                distortion_st_dev=distortion_st_dev,
                distortion_frequency=distortion_frequency,
                tween=tween,
                target_points=target_points,
            )

        extra_numbers = [0, 0]
        total_offset = [0, 0]
        for point in human_curve.points:
            x_offset, y_offset = point[0] - origin[0], point[1] - origin[1]
            extra_numbers[0] += x_offset - int(x_offset)
            extra_numbers[1] += y_offset - int(y_offset)
            if (abs(extra_numbers[0]) > 1) and (abs(extra_numbers[1]) > 1):
                self.__action.move_by_offset(
                    int(extra_numbers[0]), int(extra_numbers[1])
                )
                total_offset[0] += int(extra_numbers[0])
                total_offset[1] += int(extra_numbers[1])
                extra_numbers[0] = extra_numbers[0] - int(extra_numbers[0])
                extra_numbers[1] = extra_numbers[1] - int(extra_numbers[1])
            elif abs(extra_numbers[0]) > 1:
                self.__action.move_by_offset((int(extra_numbers[0])), 0)
                total_offset[0] += int(extra_numbers[0])
                extra_numbers[0] = extra_numbers[0] - int(extra_numbers[0])
            elif abs(extra_numbers[1]) > 1:
                self.__action.move_by_offset(0, int(extra_numbers[1]))
                total_offset[1] += int(extra_numbers[1])
                extra_numbers[1] = extra_numbers[1] - int(extra_numbers[1])
            origin[0], origin[1] = point[0], point[1]
            total_offset[0] += int(x_offset)
            total_offset[1] += int(y_offset)
            self.__action.move_by_offset(int(x_offset), int(y_offset))

        total_offset[0] += int(extra_numbers[0])
        total_offset[1] += int(extra_numbers[1])
        self.__action.move_by_offset(int(extra_numbers[0]), int(extra_numbers[1]))
        try:
            self.__action.perform()
        except MoveTargetOutOfBoundsException:
            self.__action.move_to_element(element_or_pos)
            print(
                "MoveTargetOutOfBoundsException, Cursor Moved to Point, but without Human Trajectory!"
            )

        self.origin_coordinate = [
            pre_origin[0] + total_offset[0],
            pre_origin[1] + total_offset[1],
        ]

        return [pre_origin[0] + total_offset[0], pre_origin[1] + total_offset[1]]

    @staticmethod
    def calculate_absolute_offset(element, list_of_x_and_y_offsets):
        """Calculates exact number of pixel offsets from relative values"""
        dimensions = element.size
        width, height = dimensions["width"], dimensions["height"]
        x_final = width * list_of_x_and_y_offsets[0]
        y_final = height * list_of_x_and_y_offsets[1]

        return [int(x_final), int(y_final)]

    @staticmethod
    def generate_random_curve_parameters(driver, pre_origin, post_destination):
        """Generates random parameters for the curve, the tween, number of knots, distortion, target points and boundaries"""
        viewport_width, viewport_height = driver.get_window_size().values()
        min_width, max_width = viewport_width * 0.2, viewport_width * 0.8
        min_height, max_height = viewport_height * 0.2, viewport_height * 0.8

        tween_options = [
            pytweening.easeOutExpo,
            pytweening.easeInOutQuint,
            pytweening.easeInOutSine,
            pytweening.easeInOutQuart,
            pytweening.easeInOutExpo,
            pytweening.easeInOutCubic,
            pytweening.easeInOutCirc,
            pytweening.linear,
            pytweening.easeOutSine,
            pytweening.easeOutQuart,
            pytweening.easeOutQuint,
            pytweening.easeOutCubic,
            pytweening.easeOutCirc,
        ]

        tween = random.choice(tween_options)
        offset_boundary_x = random.choice(
            random.choices(
                [range(0, 20), range(20, 60), range(60, 80)], [0.3, 0.6, 0.1]
            )[0]
        )
        offset_boundary_y = random.choice(
            random.choices(
                [range(0, 20), range(20, 60), range(60, 80)], [0.3, 0.6, 0.1]
            )[0]
        )

        knots_count = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [0.12, 0.45, 0.08, 0.07, 0.07, 0.06, 0.04, 0.04, 0.04, 0.03],
        )

        distortion_mean = random.choice(range(0, 100)) / 100
        distortion_st_dev = random.choice(range(0, 100)) / 100
        distortion_frequency = random.choice(range(25, 75)) / 100

        target_points = random.choice(
            random.choices(
                [range(25, 35), range(35, 75), range(75, 90)], [0.08, 0.8, 0.12]
            )[0]
        )

        if (
            min_width > pre_origin[0]
            or max_width < pre_origin[0]
            or min_height > pre_origin[1]
            or max_height < pre_origin[1]
        ):
            offset_boundary_x = 0
            offset_boundary_y = 0
            knots_count = 1
        if (
            min_width > post_destination[0]
            or max_width < post_destination[0]
            or min_height > post_destination[1]
            or max_height < post_destination[1]
        ):
            offset_boundary_x = 0
            offset_boundary_y = 0
            knots_count = 1

        return (
            offset_boundary_x,
            offset_boundary_y,
            knots_count,
            distortion_mean,
            distortion_st_dev,
            distortion_frequency,
            tween,
            target_points,
        )
