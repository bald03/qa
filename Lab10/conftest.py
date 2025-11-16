import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


SELENIUM_HUB_URL = "http://localhost:4444/wd/hub"


@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    driver = None

    try:
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            driver = webdriver.Remote(
                command_executor=SELENIUM_HUB_URL,
                options=options
            )

        elif browser == "firefox":
            options = FirefoxOptions()

            driver = webdriver.Remote(
                command_executor=SELENIUM_HUB_URL,
                options=options
            )

        driver.maximize_window()

        yield driver

    finally:
        if driver:
            driver.quit()
