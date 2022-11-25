import requests
import time
from datetime import datetime
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from .portals import login
from .print_util import print_clr
from colorama import Style, Fore

DEFAULT_TARGET_BROWSER = "chrome"
DEFAULT_CHROME_DRIVER_VERSION = ""  # default to latest chrome driver
DEFAULT_FIREFOX_DRIVER_VERSION = ""  # default to latest firefox driver
DEFAULT_DETECT_PORTAL_URL = "http://detectportal.firefox.com/"


@contextmanager
def create_webdriver_context(
    target_browser: str = DEFAULT_TARGET_BROWSER,
    chrome_driver_version: str = DEFAULT_CHROME_DRIVER_VERSION,
    firefox_driver_version: str = DEFAULT_FIREFOX_DRIVER_VERSION,
):
    if target_browser == "firefox":
        options = webdriver.firefox.options.Options()
        options.headless = True
        driver_path = GeckoDriverManager(
            version=firefox_driver_version,
            cache_valid_range=100,
        ).install()
        print(f"Using driver: {driver_path}")
        with webdriver.Firefox(
            options=options,
            executable_path=driver_path,
        ) as d:
            yield d
    else:  # default target
        options = webdriver.chrome.options.Options()
        options.headless = True
        driver_path = ChromeDriverManager(
            version=chrome_driver_version,
            cache_valid_range=100,
        ).install()
        print(f"Using driver: {driver_path}")
        with webdriver.Chrome(
            options=options,
            executable_path=driver_path,
        ) as d:
            yield d


def portal_connected(detect_portal_url: str):
    response = requests.get(detect_portal_url)
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


def portal_connected_print_if_changed(detect_portal_url: str, previous_state: bool):
    current_state = portal_connected(detect_portal_url)
    if current_state != previous_state:
        print_portal_status(current_state)
    return current_state


def ensure_portal_connection(
    driver: WebDriver, detect_portal_url: str = DEFAULT_DETECT_PORTAL_URL
):
    if portal_connected(detect_portal_url):
        print("Already connected")
        return

    login.try_login(driver=driver, detect_portal_url=detect_portal_url)

    if portal_connected(detect_portal_url):
        print("Login succeeded")
    else:
        print("Login failed")


def watch_portal_connection(
    driver: WebDriver,
    watch_interval: float,
    detect_portal_url: str = DEFAULT_DETECT_PORTAL_URL,
):
    print_clr(
        f"{Style.BRIGHT}Checking portal every ",
        f"{Style.BRIGHT}{Fore.CYAN}{watch_interval} ",
        f"{Style.BRIGHT}seconds.  Ctrl-c to exit.",
    )

    connected = portal_connected(detect_portal_url)
    print_portal_status(connected)

    while True:
        connected = portal_connected_print_if_changed(
            detect_portal_url=detect_portal_url,
            previous_state=connected,
        )

        if not connected:
            login.try_login(driver=driver)
            connected = portal_connected_print_if_changed(
                detect_portal_url=detect_portal_url,
                previous_state=connected,
            )
            if connected:
                print("Login succeeded")
            else:
                print("Login failed.  Exiting.")
                return
        time.sleep(watch_interval)
