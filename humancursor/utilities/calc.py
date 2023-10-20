from selenium.webdriver import Chrome, Firefox, Edge, Safari
import pytweening
import random


def calculate_absolute_offset(element, list_of_x_and_y_offsets):
    """Calculates exact number of pixel offsets from relative values"""
    dimensions = element.size
    width, height = dimensions["width"], dimensions["height"]
    x_final = width * list_of_x_and_y_offsets[0]
    y_final = height * list_of_x_and_y_offsets[1]

    return [int(x_final), int(y_final)]


def generate_random_curve_parameters(driver, pre_origin, post_destination):
    """Generates random parameters for the curve, the tween, number of knots, distortion, target points and boundaries"""
    web = False
    if isinstance(driver, (Chrome, Firefox, Edge, Safari)):
        web = True
        viewport_width, viewport_height = driver.get_window_size().values()
    else:
        viewport_width, viewport_height = driver.size()
    min_width, max_width = viewport_width * 0.15, viewport_width * 0.85
    min_height, max_height = viewport_height * 0.15, viewport_height * 0.85

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
            [range(20, 45), range(45, 75), range(75, 100)], [0.2, 0.65, 15]
        )[0]
    )
    offset_boundary_y = random.choice(
        random.choices(
            [range(20, 45), range(45, 75), range(75, 100)], [0.2, 0.65, 15]
        )[0]
    )
    knots_count = random.choices(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [0.15, 0.36, 0.17, 0.12, 0.08, 0.04, 0.03, 0.02, 0.015, 0.005],
    )[0]

    distortion_mean = random.choice(range(80, 110)) / 100
    distortion_st_dev = random.choice(range(85, 110)) / 100
    distortion_frequency = random.choice(range(25, 70)) / 100

    if web:
        target_points = random.choice(
            random.choices(
                [range(35, 45), range(45, 60), range(60, 80)], [0.53, 0.32, 0.15]
            )[0]
        )
    else:
        target_points = random.choice(
                range(90, 110)
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
