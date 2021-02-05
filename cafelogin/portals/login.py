import re
from selenium.webdriver.remote.webdriver import WebDriver
from typing import TypedDict, Callable, Sequence
from . import portal_list
from .util import wait_url_change

TRY_PORTAL_URL = "https://www.google.com/"


def try_login(driver: WebDriver) -> None:
    url = driver.current_url
    driver.get(TRY_PORTAL_URL)
    url = wait_url_change(url, driver)
    if url == TRY_PORTAL_URL:
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
