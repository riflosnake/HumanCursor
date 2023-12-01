import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from humancursor.web_cursor import WebCursor


# Disclaimer: This script is for demonstration purposes only and should not be used for any cheating activity.

def start_web_demo():
    print('Initializing Web Demo')
    driver = webdriver.Chrome()  # Creating an instance of driver
    cursor = WebCursor(driver)  # Initializing WebCursor object

    driver.get('https://humanbenchmark.com/tests/chimp')  # Going to this webpage
    driver.maximize_window()  # Maximizing window
    cursor.show_cursor()  # Injecting javascript to show a red dot over cursor

    sleep(1.5)

    start_button = driver.find_element(By.XPATH,
                                       '//button[text()="Start Test"]')  # Getting element of Start Test Button

    cursor.click_on(start_button)  # Clicking on Start Test Button

    sleep(1.2)

    for attempt in range(5):
        blocks = driver.find_elements(By.XPATH, '//div[@data-cellnumber]')  # Finding all blocks
        blocks_sorted = sorted(blocks,
                               key=lambda x: int(x.get_attribute('data-cellnumber')))  # Sorting them numerically
        for block in blocks_sorted:
            cursor.click_on(block)  # Clicking on each block in order

        continue_button = driver.find_element(By.XPATH,
                                              '//button[text()="Continue"]')  # Finding element of Continue Button
        cursor.click_on(continue_button)  # Clicking on Continue Button
        sleep(1.2)

    sleep(3)
    print('Web Demo ended')
    driver.quit()  # Quitting driver, closing window
    sys.exit()  # End script


start_web_demo()
