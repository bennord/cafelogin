import requests
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager
from typing import Sequence
from .portals import login

DETECT_PORTAL_URL = "http://detectportal.firefox.com/"
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


def portal_connected():
    response = requests.get(DETECT_PORTAL_URL)
    return response.ok and response.text.strip() == "success"


def ensure_portal_connection(driver: WebDriver):
    if portal_connected():
        print("Already connected")
        return

    login.try_login(driver=driver)

    if portal_connected():
        print("Login succeded")
    else:
        print("Login failed")
