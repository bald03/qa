import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Выбор браузера: chrome или firefox",
        choices=["chrome", "firefox"]
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    
    hub_url = "http://localhost:4444/wd/hub"
    
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--no-sandbox")
        options.set_preference("dom.disable_beforeunload", True)
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser}")
    
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options,
        keep_alive=True
    )
    
    driver.implicitly_wait(10)  # Неявное ожидание элементов
    driver.set_page_load_timeout(60)  # Таймаут загрузки страницы
    driver.set_script_timeout(60)  # Таймаут выполнения скриптов
    
    try:
        driver.maximize_window()
    except Exception:
        driver.set_window_size(1920, 1080)
    
    yield driver
    
    driver.quit()
