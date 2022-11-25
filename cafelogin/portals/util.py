from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def wait_url_change(url: str, driver: WebDriver):
    wait = WebDriverWait(driver, 3)
    wait.until(expected_conditions.url_changes(url))
    url = driver.current_url
    return url
