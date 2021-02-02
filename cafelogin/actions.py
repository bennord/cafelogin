import requests
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager
from typing import Sequence

DETECT_PORTAL_URL = "http://detectportal.firefox.com/"
TRY_PORTAL_URL = "https://www.google.com/"
DEFAULT_DRIVER_VERSION = "v0.29.0"


def install_webdriver(version: str = DEFAULT_DRIVER_VERSION) -> str:
    return GeckoDriverManager(
        version=version,
        cache_valid_range=100,
        print_first_line=False,
    ).install()


@contextmanager
def create_webdriver_context(driver_version: str = DEFAULT_DRIVER_VERSION):
    options = webdriver.firefox.options.Options()
    options.headless = True
    with webdriver.Firefox(
        options=options,
        executable_path=install_webdriver(version=driver_version),
    ) as d:
        yield d


def wait_url_change(url: str, driver: WebDriver):
    wait = WebDriverWait(driver, 3)
    wait.until(expected_conditions.url_changes(url))
    url = driver.current_url
    return url


def portal_connected():
    response = requests.get(DETECT_PORTAL_URL)
    return response.ok and response.text.strip() == "success"


def try_portal_login(driver: WebDriver):
    url = driver.current_url
    print(f"Url: {url}")
    print(f"Test navigation to: {TRY_PORTAL_URL}")
    driver.get(TRY_PORTAL_URL)
    url = wait_url_change(url, driver)
    if url == TRY_PORTAL_URL:
        return
    print(f"Url: {url}")
    print(f"Click button_next_page")
    driver.find_element_by_id("button_next_page").click()
    url = wait_url_change(url, driver)
    print(f"Url: {url}")
    print(f"Click button_accept")
    driver.find_element_by_id("button_accept").click()
    url = wait_url_change(url, driver)
    print(f"Url: {url}")


def ensure_portal_connection(driver: WebDriver):
    if portal_connected():
        print("Already connected")
        return

    try_portal_login(driver=driver)

    if portal_connected():
        print("Login success")
    else:
        print("Login failed")
