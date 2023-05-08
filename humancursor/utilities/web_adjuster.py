import random

from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains

from humancursor.utilities.human_curve_generator import HumanizeMouseTrajectory
from humancursor.utilities.calc import generate_random_curve_parameters, calculate_absolute_offset


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
        steady=False
    ):
        """Moves the humancursor, trying to mimic human behaviour!"""
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
                abs_exact_offset = calculate_absolute_offset(
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
        ) = generate_random_curve_parameters(
            self.__driver, [origin[0], origin[1]], [x, y]
        )
        if steady:
            offset_boundary_x, offset_boundary_y = 10, 10
            distortion_mean, distortion_st_dev, distortion_frequency = 1.2, 1.2, 1
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
