"""
Конфигурационный файл pytest (conftest.py)

Этот файл содержит общие настройки и фикстуры для всех тестов.
Фикстуры - это функции, которые выполняются до и после тестов.

Настроен для работы с Selenium Grid через RemoteWebDriver.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


# URL Selenium Hub
SELENIUM_HUB_URL = "http://localhost:4444/wd/hub"


@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    """
    Фикстура для создания и управления веб-драйвером Selenium через RemoteWebDriver.
    
    Scope "function" означает, что драйвер создается заново для каждого теста.
    Это обеспечивает изоляцию тестов друг от друга.
    
    Параметр params=["chrome", "firefox"] обеспечивает запуск каждого теста
    в обоих браузерах.
    
    Процесс работы:
    1. Создается RemoteWebDriver, подключенный к Selenium Grid Hub
    2. Выбирается браузер на основе параметра (chrome или firefox)
    3. Окно браузера максимизируется
    4. Драйвер передается в тест через параметр driver
    5. После завершения теста браузер закрывается (driver.quit())
    
    Args:
        request: Объект pytest request для доступа к параметрам фикстуры
    
    Returns:
        WebDriver: Экземпляр RemoteWebDriver для управления браузером
    """
    browser = request.param
    driver = None
    
    try:
        if browser == "chrome":
            # Настройка опций для Chrome
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # Создаем RemoteWebDriver для Chrome
            driver = webdriver.Remote(
                command_executor=SELENIUM_HUB_URL,
                options=options
            )
            
        elif browser == "firefox":
            # Настройка опций для Firefox
            options = FirefoxOptions()
            # Для Firefox в Docker обычно не требуются дополнительные аргументы
            # maximize_window() будет вызван ниже
            
            # Создаем RemoteWebDriver для Firefox
            driver = webdriver.Remote(
                command_executor=SELENIUM_HUB_URL,
                options=options
            )
        
        # Максимизируем окно браузера для лучшей видимости элементов
        driver.maximize_window()
        
        # yield передает управление тесту, после завершения теста выполнится код после yield
        yield driver
        
    finally:
        # Закрываем браузер после завершения теста
        if driver:
            driver.quit()
