import requests
import time
from datetime import datetime
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from typing import Sequence
from .portals import login
from .portals.util import DETECT_PORTAL_URL
from .print_util import print_clr
from colorama import Style, Fore

DEFAULT_TARGET_BROWSER = "chrome"
DEFAULT_CHROME_DRIVER_VERSION = "104.0.5112.79"
DEFAULT_FIREFOX_DRIVER_VERSION = "v0.29.0"


@contextmanager
def create_webdriver_context(
    target_browser: str = DEFAULT_TARGET_BROWSER,
    chrome_driver_version: str = DEFAULT_CHROME_DRIVER_VERSION,
    firefox_driver_version: str = DEFAULT_FIREFOX_DRIVER_VERSION,
):
    if target_browser == "firefox":
        options = webdriver.firefox.options.Options()
        options.headless = True
        with webdriver.Firefox(
            options=options,
            executable_path=GeckoDriverManager(
                version=firefox_driver_version,
                cache_valid_range=100,
            ).install(),
        ) as d:
            yield d
    else:  # default target
        options = webdriver.chrome.options.Options()
        options.headless = True
        with webdriver.Chrome(
            options=options,
            executable_path=ChromeDriverManager(
                version=chrome_driver_version,
                cache_valid_range=100,
            ).install(),
        ) as d:
            yield d


def portal_connected():
    response = requests.get(DETECT_PORTAL_URL)
    return response.ok and response.text.strip() == "success"


def print_portal_status(connected: bool):
    if connected:
        print_clr(
            f"{Fore.GREEN}{datetime.now()}",
            f"{Fore.GREEN}{Style.DIM} - Portal connection up",
        )
    else:
        print_clr(
            f"{Fore.YELLOW}{datetime.now()}",
            f"{Fore.YELLOW}{Style.DIM} - Portal connection down",
        )


def portal_connected_print_if_changed(previous_state: bool):
    current_state = portal_connected()
    if current_state != previous_state:
        print_portal_status(current_state)
    return current_state


def ensure_portal_connection(driver: WebDriver):
    if portal_connected():
        print("Already connected")
        return

    login.try_login(driver=driver)

    if portal_connected():
        print("Login succeeded")
    else:
        print("Login failed")


def watch_portal_connection(driver: WebDriver, watch_interval: float):
    print_clr(
        f"{Style.BRIGHT}Checking portal every ",
        f"{Style.BRIGHT}{Fore.CYAN}{watch_interval} ",
        f"{Style.BRIGHT}seconds.  Ctrl-c to exit.",
    )

    connected = portal_connected()
    print_portal_status(connected)

    while True:
        connected = portal_connected_print_if_changed(connected)

        if not connected:
            login.try_login(driver=driver)
            connected = portal_connected_print_if_changed(connected)
            if connected:
                print("Login succeeded")
            else:
                print("Login failed.  Exiting.")
                return
        time.sleep(watch_interval)
