from selenium.webdriver.remote.webdriver import WebDriver
from .util import wait_url_change


def login(driver: WebDriver):
    url = driver.current_url
    print(f"Click button_next_page")
    driver.find_element_by_id("button_next_page").click()
    url = wait_url_change(url, driver)
    print(f"Url: {url}")
    print(f"Click button_accept")
    driver.find_element_by_id("button_accept").click()
    url = wait_url_change(url, driver)
    print(f"Url: {url}")
