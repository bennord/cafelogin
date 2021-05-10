from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from .util import wait_url_change


def login(driver: WebDriver):
    url = driver.current_url
    try:
        print(f"Find button_next_page")
        button_next_page = driver.find_element_by_id("button_next_page")
        button_next_page.click()
        url = wait_url_change(url, driver)
        print(f"Url: {url}")
    except NoSuchElementException:
        print(f"Not found: button_next_page")

    try:
        print(f"Find button_accept")
        button_accept = driver.find_element_by_id("button_accept")
        button_accept.click()
        url = wait_url_change(url, driver)
        print(f"Url: {url}")
    except NoSuchElementException:
        print(f"Not found: button_accept")
