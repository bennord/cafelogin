import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from typing import TypedDict, Callable, Sequence

TRY_PORTAL_URL = "https://www.google.com/"


class Portal(TypedDict):  # pylint: disable=inherit-non-class
    pattern: str
    login: Callable[[WebDriver], None]


def wait_url_change(url: str, driver: WebDriver):
    wait = WebDriverWait(driver, 3)
    wait.until(expected_conditions.url_changes(url))
    url = driver.current_url
    return url


def login_wi2(driver: WebDriver):
    url = driver.current_url
    print(f"Click button_next_page")
    driver.find_element_by_id("button_next_page").click()
    url = wait_url_change(url, driver)
    print(f"Url: {url}")
    print(f"Click button_accept")
    driver.find_element_by_id("button_accept").click()
    url = wait_url_change(url, driver)
    print(f"Url: {url}")


# A dictionary mapping portals to their login scipts
portals: Sequence[Portal] = [{"pattern": r"service\.wi2\.ne\.jp", "login": login_wi2}]


def try_login(driver: WebDriver) -> None:
    url = driver.current_url
    driver.get(TRY_PORTAL_URL)
    url = wait_url_change(url, driver)
    if url == TRY_PORTAL_URL:
        print("Already connected")
        return

    for p in portals:
        if re.search(p["pattern"], url) is not None:
            print(
                f"Known portal found:\n\tUrl: {url}\n\tMatch: {p['pattern']}\nAttempting to login..."
            )
            p["login"](driver)
            return

    print(f"Unknown portal found:\n\tUrl: {url}\n\tMatch: None")
