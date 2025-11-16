"""
Конфигурационный файл pytest (conftest.py)

Этот файл содержит общие настройки и фикстуры для всех тестов.
Фикстуры - это функции, которые выполняются до и после тестов.
"""

import pytest
from selenium import webdriver


def pytest_addoption(parser):
    """
    Добавляет опцию командной строки для выбора браузера.
    
    Использование:
        pytest --browser=chrome
        pytest --browser=firefox
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Выбор браузера: chrome или firefox",
        choices=["chrome", "firefox"]
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Фикстура для создания и управления веб-драйвером Selenium через RemoteWebDriver.
    
    Scope "function" означает, что драйвер создается заново для каждого теста.
    Это обеспечивает изоляцию тестов друг от друга.
    
    Процесс работы:
    1. Определяется браузер из параметра командной строки (--browser)
    2. Создается RemoteWebDriver, который подключается к Selenium Grid Hub
    3. Hub перенаправляет запрос на соответствующий node (Chrome или Firefox)
    4. Окно браузера максимизируется
    5. Драйвер передается в тест через параметр driver
    6. После завершения теста браузер закрывается (driver.quit())
    
    Args:
        request: Объект pytest request для доступа к параметрам командной строки
    
    Returns:
        WebDriver: Экземпляр RemoteWebDriver для управления браузером через Selenium Grid
    
    Note:
        Selenium Grid Hub должен быть запущен на localhost:4444
        Запуск: docker-compose up -d
    """
    # Получаем выбранный браузер из параметра командной строки
    browser = request.config.getoption("--browser")
    
    # URL Selenium Grid Hub
    hub_url = "http://localhost:4444/wd/hub"
    
    # Создаем опции в зависимости от выбранного браузера
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        # Добавляем опции для работы в контейнере
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        # Добавляем опции для работы в контейнере
        options.add_argument("--no-sandbox")
        # Устанавливаем размер окна для Firefox
        options.set_preference("dom.disable_beforeunload", True)
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser}")
    
    # Создаем RemoteWebDriver, который подключается к Selenium Grid Hub
    # Hub автоматически перенаправит запрос на соответствующий node (Chrome или Firefox)
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options,
        keep_alive=True
    )
    
    # Устанавливаем таймауты для стабильности работы
    driver.implicitly_wait(10)  # Неявное ожидание элементов
    driver.set_page_load_timeout(60)  # Таймаут загрузки страницы
    driver.set_script_timeout(60)  # Таймаут выполнения скриптов
    
    # Максимизируем окно браузера для лучшей видимости элементов
    # Используем try-except для обработки возможных ошибок
    try:
        driver.maximize_window()
    except Exception:
        # Если не удалось максимизировать, устанавливаем размер окна
        driver.set_window_size(1920, 1080)
    
    # yield передает управление тесту, после завершения теста выполнится код после yield
    yield driver
    
    # Закрываем браузер после завершения теста
    driver.quit()
