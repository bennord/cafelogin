from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager
from typing import Sequence


with webdriver.Firefox(executable_path=GeckoDriverManager().install()) as driver:
    wait = WebDriverWait(driver, 3)
    driver.get("https://service.wi2.ne.jp/freewifi/starbucks/index.html")
    print(driver.current_url)
    driver.find_element_by_id("button_next_page").click()
    print(driver.current_url)
    driver.find_element_by_id("button_accept").click()
    wait.until(
        expected_conditions.presence_of_all_elements_located(
            (By.CLASS_NAME, "main_img")
        )
    )
    print(driver.current_url)
    print("SUCCESS")
