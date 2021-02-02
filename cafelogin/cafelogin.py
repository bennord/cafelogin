import requests
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.firefox import GeckoDriverManager
from typing import Sequence

DETECT_PORTAL_URL = "http://detectportal.firefox.com/"


def wait_url_change(url: str, driver: WebDriver):
    wait = WebDriverWait(driver, 3)
    wait.until(expected_conditions.url_changes(url))
    url = driver.current_url
    print(f"Url: {url}")
    return url


def portal_connected():
    response = requests.get(DETECT_PORTAL_URL)
    return response.ok and response.text.strip() == "success"


def try_portal_login():
    with webdriver.Firefox(
        executable_path=GeckoDriverManager(
            version="v0.29.0", cache_valid_range=100
        ).install()
    ) as driver:
        url = driver.current_url
        print(f"Nav to: {DETECT_PORTAL_URL}")
        driver.get(DETECT_PORTAL_URL)
        url = wait_url_change(url, wait)
        print(f"Click button_next_page")
        driver.find_element_by_id("button_next_page").click()
        url = wait_url_change(url, wait)
        print(f"Click button_accept")
        driver.find_element_by_id("button_accept").click()
        url = wait_url_change(url, wait)


def ensure_portal_connection():
    if portal_connected():
        print("Already connected")
        return

    try_portal_login()

    if portal_connected():
        print("Login success")
    else:
        print("Login failed")


def run():
    ensure_portal_connection()