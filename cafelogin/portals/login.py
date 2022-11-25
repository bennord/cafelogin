import re
from selenium.webdriver.remote.webdriver import WebDriver
from typing import TypedDict, Callable, Sequence
from . import portal_list
from .util import wait_url_change


def try_login(driver: WebDriver, detect_portal_url: str) -> None:
    url = driver.current_url
    driver.get(detect_portal_url)
    url = wait_url_change(url, driver)
    if url == detect_portal_url:
        print("Already connected")
        return

    for p in portal_list.portals:
        if re.search(p["pattern"], url) is not None:
            print(
                f"Known portal found:\n\tUrl: {url}\n\tMatch: {p['pattern']}\nAttempting to login..."
            )
            p["login"](driver)
            return

    print(f"Unknown portal found:\n\tUrl: {url}\n\tMatch: None")
