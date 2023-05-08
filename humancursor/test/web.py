import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from humancursor.web_cursor import WebCursor


def start_web_demo():
    # Disclaimer: This script is for demonstration purposes only and should not be used for any cheating activity.
    driver = webdriver.Chrome()
    cursor = WebCursor(driver)

    driver.get('https://humanbenchmark.com/tests/chimp')
    driver.maximize_window()
    cursor.show_cursor()

    sleep(2)

    start_button = driver.find_element(By.XPATH, '//button[text()="Start Test"]')

    cursor.click_on(start_button)

    sleep(2)

    for attempt in range(5):
        blocks = driver.find_elements(By.XPATH, '//div[@data-cellnumber]')
        blocks_sorted = sorted(blocks, key=lambda x: int(x.get_attribute('data-cellnumber')))
        for block in blocks_sorted:
            cursor.click_on(block)

        continue_button = driver.find_element(By.XPATH, '//button[text()="Continue"]')
        cursor.click_on(continue_button)
        sleep(3)

    sleep(10)
    driver.quit()
    sys.exit()
