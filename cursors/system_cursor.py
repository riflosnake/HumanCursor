from time import sleep
import random
import pyautogui

from cursors.utilities.human_curve_generator import HumanizeMouseTrajectory


class SystemCursor:
    def __init__(self):
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0.015

    @staticmethod
    def move_to(point: list, duration: int = None, human_curve=None):
        """Moves to certain coordinates of screen"""
        from_point = pyautogui.position()
        if not human_curve:
            human_curve = HumanizeMouseTrajectory(from_point, point)

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
