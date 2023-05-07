from time import sleep
import random
import pyautogui

from humancursor.utilities.human_curve_generator import HumanizeMouseTrajectory
from humancursor.utilities.calc import generate_random_curve_parameters


class SystemCursor:
    def __init__(self):
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0

    @staticmethod
    def move_to(point: list, duration: int = None, human_curve=None):
        """Moves to certain coordinates of screen"""
        from_point = pyautogui.position()

        if not human_curve:
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
                pyautogui, from_point, point
            )
            human_curve = HumanizeMouseTrajectory(
                from_point,
                point,
                offset_boundary_x=offset_boundary_x,
                offset_boundary_y=offset_boundary_y,
                knots_count=knots_count,
                distortion_mean=distortion_mean,
                distortion_st_dev=distortion_st_dev,
                distortion_frequency=distortion_frequency,
                tween=tween,
                target_points=target_points,
            )

        if duration is None:
            duration = random.uniform(0.5, 2.0)
        pyautogui.PAUSE = duration / len(human_curve.points)
        for pnt in human_curve.points:
            pyautogui.moveTo(pnt)
        pyautogui.moveTo(point)

    def click_on(self, point: list, clicks: int = 1):
        """Clicks a specified number of times, on the specified coordinates"""
        self.move_to(point)
        for _ in range(clicks):
            pyautogui.click()
            sleep(random.uniform(0.150, 0.300))

    def drag_and_drop(self, from_point: list, to_point: list):
        """Drags from a certain point, and releases to another"""
        self.move_to(from_point)
        pyautogui.mouseDown()
        self.move_to(to_point)
        pyautogui.mouseUp()
