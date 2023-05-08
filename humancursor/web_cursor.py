from time import sleep
import random

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from humancursor.utilities.web_adjuster import WebAdjuster


class WebCursor:
    def __init__(self, driver):
        self.__driver = driver
        self.__action = ActionChains(self.__driver, duration=1500)
        self.human = WebAdjuster(self.__driver)
        self.origin_coordinates = [0, 0]

    def move_to(
        self,
        element: WebElement or list,
        relative_position: list = None,
        absolute_offset: bool = False,
        origin_coordinates=None,
        steady=False
    ):
        """Moves to element or coordinates with human curve"""
        if not self.scroll_into_view_of_element(element):
            return False
        if origin_coordinates is None:
            origin_coordinates = self.origin_coordinates
        self.origin_coordinates = self.human.move_to(
            element,
            origin_coordinates=origin_coordinates,
            absolute_offset=absolute_offset,
            relative_position=relative_position,
            steady=steady
        )
        return self.origin_coordinates

    def click_on(
        self,
        element: WebElement or list,
        number_of_clicks: int = 1,
        relative_position: list = None,
        absolute_offset: bool = False,
        origin_coordinates=None,
        steady=False
    ):
        """Moves to element or coordinates with human curve, and clicks on it a specified number of times, default is 1"""
        self.move_to(
            element,
            origin_coordinates=origin_coordinates,
            absolute_offset=absolute_offset,
            relative_position=relative_position,
            steady=steady
        )
        self.click(number_of_clicks)
        return True

    def click(self, number_of_clicks=1):
        """Performs the click action"""
        for _ in range(number_of_clicks):
            self.__action.click().pause(random.randint(200, 300) / 1000)
        self.__action.perform()
        return True

    def move_by_offset(self, x: int, y: int, steady=False):
        """Moves the cursor with human curve, by specified number of x and y pixels"""
        self.origin_coordinates = self.human.move_to([x, y], absolute_offset=True, steady=steady)
        return True

    def drag_and_drop(
        self,
        drag_from_element: WebElement or list,
        drag_to_element: WebElement or list,
        drag_from_relative_position: list = None,
        drag_to_relative_position: list = None,
        steady=False
    ):
        """Moves to element or coordinates, clicks and holds, dragging it to another element, with human curve"""
        if drag_from_relative_position is None:
            self.move_to(drag_from_element)
        else:
            self.move_to(
                drag_from_element, relative_position=drag_from_relative_position
            )

        if drag_to_element is None:
            self.__action.click().perform()
        else:
            self.__action.click_and_hold().perform()
            if drag_to_relative_position is None:
                self.move_to(drag_to_element, steady=steady)
            else:
                self.move_to(
                    drag_to_element, relative_position=drag_to_relative_position, steady=steady
                )
            self.__action.release().perform()

        return True

    def control_scroll_bar(
        self,
        scroll_bar_element: WebElement,
        amount_by_percentage: list,
        orientation: str = "horizontal",
        steady=False
    ):
        """Adjusts any scroll bar on the webpage, by the amount you want in float number from 0 to 1
        representing percentage of fullness, orientation of the scroll bar must also be defined by user
        horizontal or vertical"""
        direction = True if orientation == "horizontal" else False

        self.move_to(scroll_bar_element)
        self.__action.click_and_hold().perform()
        # TODO: this needs rework, it will be more natural if it goes out of scroll bar, up or down randomly
        if direction:
            self.move_to(
                scroll_bar_element,
                relative_position=[amount_by_percentage, random.randint(0, 100) / 100],
                steady=steady
            )
        else:
            self.move_to(
                scroll_bar_element,
                relative_position=[random.randint(0, 100) / 100, amount_by_percentage],
                steady=steady
            )

        self.__action.release().perform()

        return True

    def scroll_into_view_of_element(self, element: WebElement):
        """Scrolls the element into viewport, if not already in it"""
        if isinstance(element, WebElement):
            is_in_viewport = self.__driver.execute_script(
                """
              var element = arguments[0];
              var rect = element.getBoundingClientRect();
              return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
              );
            """,
                element,
            )
            if not is_in_viewport:
                self.__driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                    element,
                )
                sleep(random.uniform(0.8, 1.4))
            return True
        elif isinstance(element, list):
            """User should input correct coordinates of x and y, cant take any action"""
            return True
        else:
            print("Incorrect Element or Coordinates values!")
            return False

    def show_cursor(self):
        self.__driver.execute_script('''
        let dot;
            function displayRedDot() {
              // Get the cursor position
              const x = event.clientX;
              const y = event.clientY;
            
              if (!dot) {
                // Create a new div element for the red dot if it doesn't exist
                dot = document.createElement("div");
                // Style the dot with CSS
                dot.style.position = "fixed";
                dot.style.width = "5px";
                dot.style.height = "5px";
                dot.style.borderRadius = "50%";
                dot.style.backgroundColor = "red";
                // Add the dot to the page
                document.body.appendChild(dot);
              }
            
              // Update the dot's position
              dot.style.left = x + "px";
              dot.style.top = y + "px";
            }
            
            // Add event listener to update the dot's position on mousemove
            document.addEventListener("mousemove", displayRedDot);''')
