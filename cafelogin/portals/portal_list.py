from selenium.webdriver.remote.webdriver import WebDriver
from typing import TypedDict, Callable, Sequence
from . import portal_wi2


class Portal(TypedDict):  # pylint: disable=inherit-non-class
    pattern: str
    login: Callable[[WebDriver], None]


# A List mapping portals to their login scipts
portals: Sequence[Portal] = [
    {"pattern": r"service\.wi2\.ne\.jp", "login": portal_wi2.login}
]
