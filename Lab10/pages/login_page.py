"""
Page Object класс для работы со страницей авторизации.

Этот класс инкапсулирует всю логику взаимодействия со страницей входа на сайте.
Использует паттерн Page Object Model для разделения логики работы со страницей и тестов.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Класс для работы со страницей авторизации AutomationExercise.com.
    
    Содержит:
    - Локаторы элементов страницы (селекторы для поиска элементов)
    - Методы для взаимодействия с элементами (клики, ввод текста)
    - Методы для проверки состояния (успешный вход, ошибки)
    """
    # ==================== ЛОКАТОРЫ ЭЛЕМЕНТОВ ====================
    # Локаторы - это селекторы для поиска элементов на странице
    # Формат: (тип_локатора, селектор)
    
    # Ссылка для перехода на страницу входа (в меню сайта)
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    
    # Поле ввода email для авторизации
    # Используется data-qa атрибут - специальный атрибут для тестирования
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    
    # Поле ввода пароля
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    
    # Кнопка "Login" для отправки формы авторизации
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    
    # Элемент, указывающий на успешную авторизацию (ссылка Logout в меню)
    # Используется XPath с несколькими вариантами для надежности
    SUCCESS_MESSAGE = (By.XPATH, "//li/a[contains(@href, '/logout')] | //a[contains(@href, '/logout')]")
    
    # Сообщение об ошибке при неверных данных
    # Ищет параграф с красным цветом текста или в форме логина
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p[style*='color: red'], .login-form p")

    def __init__(self, driver):
        """
        Конструктор класса LoginPage.
        
        Args:
            driver: Экземпляр WebDriver для управления браузером
        """
        self.driver = driver

    def open(self, base_url):
        """
        Открывает указанный URL в браузере.
        
        Args:
            base_url (str): URL адрес для открытия
        """
        self.driver.get(base_url)

    def open_login_page(self):
        """
        Переходит на страницу авторизации.
        
        Находит и кликает на ссылку "Signup / Login" в меню сайта.
        Использует явное ожидание для надежности.
        """
        login_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_LINK)
        )
        login_link.click()

    def login(self, email, password):
        """
        Выполняет авторизацию пользователя.
        
        Процесс:
        1. Ожидает появления поля email (явное ожидание до 10 секунд)
        2. Очищает поле и вводит email
        3. Очищает поле и вводит пароль
        4. Кликает на кнопку входа
        5. Ждет загрузки страницы после авторизации
        
        Args:
            email (str): Email пользователя для авторизации
            password (str): Пароль пользователя
        
        Note:
            Используется time.sleep для ожидания загрузки страницы.
            В продакшене лучше использовать явные ожидания WebDriverWait.
        """
        # Ожидаем появления поля email с явным ожиданием (до 10 секунд)
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        # Очищаем поле перед вводом (на случай, если там уже есть текст)
        email_input.clear()
        # Вводим email
        email_input.send_keys(email)
        
        # Находим поле пароля (без явного ожидания, т.к. оно на той же странице)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        
        # Находим и кликаем кнопку входа
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
        
        # Ждем перехода после авторизации
        # Небольшая задержка для загрузки страницы после авторизации
        # В идеале здесь должно быть явное ожидание появления элемента после входа
        time.sleep(2)

    def get_success_message(self):
        """
        Получает сообщение об успешной авторизации.
        
        Ищет элемент, указывающий на успешный вход (обычно ссылка "Logout" 
        или текст "Logged in as [имя пользователя]").
        
        Использует несколько стратегий поиска для надежности:
        1. Поиск ссылки Logout
        2. Поиск текста в родительском элементе
        3. Поиск через ancestor (предок) элемента
        4. Альтернативный поиск по тексту
        
        Returns:
            str: Текст сообщения об успешном входе или None, если не найдено
        
        Note:
            Метод использует fallback механизм - если один способ не работает,
            пробует альтернативные варианты.
        """
        try:
            # Стратегия 1: Ищем ссылку Logout (основной признак успешной авторизации)
            success_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)
            )
            
            # Стратегия 2: Получаем текст из родительского элемента (li)
            # Родительский элемент обычно содержит полный текст "Logged in as [имя]"
            try:
                parent = success_element.find_element(By.XPATH, "./..")
                parent_text = parent.text.strip()
                # Если родительский элемент содержит "Logged in as", возвращаем его
                if "Logged in as" in parent_text:
                    return parent_text
            except:
                pass
            
            # Стратегия 3: Ищем в предке элемента (ancestor)
            # Используем XPath для поиска ближайшего родителя li
            try:
                li_element = success_element.find_element(By.XPATH, "./ancestor::li[1]")
                li_text = li_element.text.strip()
                if "Logged in as" in li_text:
                    return li_text
            except:
                pass
            
            # Стратегия 4: Если нашли только ссылку "Logout", это тоже признак успешного входа
            # Возвращаем текст ссылки (обычно "Logout")
            return success_element.text.strip()
        except:
            # Стратегия 5: Альтернативный способ - ищем текст "Logged in as" в любом месте страницы
            try:
                logged_in_text = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Logged in as')] | //a[contains(@href, '/logout')]/ancestor::li[1]"))
                )
                return logged_in_text.text.strip()
            except:
                return None

    def get_error_message(self):
        """
        Получает сообщение об ошибке при неудачной авторизации.
        
        Ищет элемент с сообщением об ошибке (обычно красный текст).
        
        Returns:
            str: Текст сообщения об ошибке или None, если не найдено
        """
        try:
            # Ожидаем появления видимого элемента с ошибкой (до 5 секунд)
            error_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text.strip()
        except:
            return None

    def is_logged_in(self):
        """
        Проверяет, авторизован ли пользователь.
        
        Проверяет наличие элементов, указывающих на успешную авторизацию:
        - Ссылка "Logout" в меню
        - Текст "Logged in as" в меню
        
        Returns:
            bool: True если пользователь авторизован, False в противном случае
        
        Note:
            Использует несколько стратегий проверки для надежности.
        """
        try:
            # Стратегия 1: Проверяем наличие ссылки Logout - основной признак успешной авторизации
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except:
            # Стратегия 2: Альтернативная проверка - ищем текст "Logged in as" или ссылку logout в меню
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/logout')] | //li[contains(text(), 'Logged in as')]"))
                )
                return True
            except:
                return False
