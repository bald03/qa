"""
Page Object класс для работы с корзиной и продуктами.

Этот класс инкапсулирует логику работы с:
- Страницей продуктов
- Добавлением товаров в корзину
- Модальными окнами
- Страницей корзины
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class CartPage:
    """
    Класс для работы с корзиной и продуктами на AutomationExercise.com.
    
    Основные функции:
    - Поиск и добавление товаров в корзину
    - Работа с модальными окнами
    - Навигация по корзине
    - Получение информации о товарах в корзине
    """
    PRODUCTS_LINK = (By.CSS_SELECTOR, "a[href='/products']")
    PRODUCT_ITEM = (By.CSS_SELECTOR, ".productinfo, .single-products")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a.add-to-cart, .overlay-content a")
    VIEW_CART_LINK = (By.XPATH, "//a[contains(@href, '/view_cart')] | //u[contains(text(), 'View Cart')] | //a[contains(text(), 'View Cart')]")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "button.close-modal, .btn-success")
    CART_MODAL_MESSAGE = (By.CSS_SELECTOR, ".modal-body p, .modal-content p")
    CART_PAGE_PRODUCTS = (By.CSS_SELECTOR, "#cart_info_table tbody tr, .cart_info tbody tr")
    PRODUCT_NAME_IN_CART = (By.CSS_SELECTOR, ".cart_description h4 a, .cart_description a")
    PRODUCT_PRICE_IN_CART = (By.CSS_SELECTOR, ".cart_price p, .cart_price")
    PRODUCT_QUANTITY_IN_CART = (By.CSS_SELECTOR, ".cart_quantity button, .cart_quantity")
    CART_TOTAL = (By.CSS_SELECTOR, ".cart_total_price, .cart_total")

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def open(self, base_url):
        self.driver.get(base_url)

    def open_products_page(self):
        products_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PRODUCTS_LINK)
        )
        products_link.click()

    def add_product_to_cart_by_name(self, product_name):
        """
        Добавляет товар в корзину по его названию.
        
        Процесс:
        1. Находит все продукты на странице
        2. Ищет продукт с указанным названием (поиск нечувствителен к регистру)
        3. Наводит мышь на продукт (для появления overlay с кнопкой)
        4. Находит и кликает кнопку "Add to cart"
        5. Использует JavaScript клик для надежности
        
        Args:
            product_name (str): Название товара для добавления в корзину
        
        Returns:
            bool: True если товар успешно добавлен, False если товар не найден
        
        Note:
            Использует несколько стратегий поиска кнопки "Add to cart":
            - Поиск внутри элемента продукта
            - Поиск в overlay элементе
            - Поиск по XPath с текстом
            JavaScript клик используется для обхода проблем с перекрытием элементов.
        """
        # Шаг 1: Находим все продукты на странице с явным ожиданием
        products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.PRODUCT_ITEM)
        )
        
        # Шаг 2: Перебираем все продукты и ищем нужный по названию
        for product in products:
            try:
                # Получаем весь текст продукта (название, цена и т.д.)
                product_text = product.text.lower()
                
                # Проверяем, содержится ли искомое название в тексте продукта
                # Поиск нечувствителен к регистру (используем .lower())
                if product_name.lower() in product_text:
                    # Шаг 3: Наводим мышь на продукт
                    # Это необходимо для появления overlay с кнопкой "Add to cart"
                    self.actions.move_to_element(product).perform()
                    
                    # Шаг 4: Ждем появления overlay с кнопкой
                    # Небольшая задержка для анимации появления overlay
                    time.sleep(0.5)
                    
                    # Шаг 5: Пытаемся найти кнопку "Add to cart" разными способами
                    try:
                        # Стратегия 1: Ищем кнопку внутри элемента продукта
                        add_button = product.find_element(*self.ADD_TO_CART_BUTTON)
                    except:
                        # Стратегия 2: Если не нашли, ищем в overlay элементе
                        try:
                            overlay = product.find_element(By.CSS_SELECTOR, ".overlay-content, .overlay")
                            add_button = overlay.find_element(*self.ADD_TO_CART_BUTTON)
                        except:
                            # Стратегия 3: Последняя попытка - ищем по тексту через XPath
                            add_button = self.driver.find_element(By.XPATH, f"//a[contains(@class, 'add-to-cart') and contains(., '{product_name}')]")
                    
                    # Шаг 6: Используем JavaScript клик для надежности
                    # Это обходит проблемы с перекрытием элементов другими элементами
                    self.driver.execute_script("arguments[0].click();", add_button)
                    return True
            except Exception as e:
                # Если произошла ошибка при обработке продукта, переходим к следующему
                continue
        
        # Если товар не найден, возвращаем False
        return False

    def wait_for_cart_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CART_MODAL_MESSAGE)
        )

    def get_cart_modal_message(self):
        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.CART_MODAL_MESSAGE)
            )
            return message.text.strip()
        except:
            return None

    def go_to_cart(self):
        """
        Переходит на страницу корзины.
        
        Обрабатывает ситуацию, когда модальное окно с сообщением о добавлении
        товара может перекрывать ссылку "View Cart". В этом случае используется
        JavaScript клик для обхода проблемы.
        
        Note:
            Использует JavaScript клик для надежности, так как модальное окно
            может перекрывать ссылку, делая обычный клик невозможным.
        """
        # Пытаемся определить, открыто ли модальное окно
        try:
            # Проверяем наличие модального окна (короткое ожидание - 2 секунды)
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cartModal"))
            )
            # Если модальное окно открыто, используем JavaScript клик
            # Это обходит проблему перекрытия элемента модальным окном
            view_cart_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.VIEW_CART_LINK)
            )
            self.driver.execute_script("arguments[0].click();", view_cart_link)
        except:
            # Если модальное окно уже закрыто или не появилось, используем обычный клик
            view_cart_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.VIEW_CART_LINK)
            )
            view_cart_link.click()

    def continue_shopping(self):
        try:
            # Ждем появления модального окна
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cartModal, .modal"))
            )
            # Ищем кнопку "Continue Shopping" или закрываем модальное окно
            try:
                continue_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
                )
                self.driver.execute_script("arguments[0].click();", continue_button)
            except:
                # Альтернативный способ - закрываем модальное окно через кнопку закрытия
                close_button = self.driver.find_element(By.CSS_SELECTOR, "button.close, .modal-header button")
                self.driver.execute_script("arguments[0].click();", close_button)
            # Ждем закрытия модального окна
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "#cartModal, .modal.show"))
            )
        except:
            pass

    def get_cart_item_names(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_PAGE_PRODUCTS)
        )
        items = self.driver.find_elements(*self.PRODUCT_NAME_IN_CART)
        return [item.text.strip() for item in items]

    def get_cart_item_prices(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_PAGE_PRODUCTS)
        )
        prices = self.driver.find_elements(*self.PRODUCT_PRICE_IN_CART)
        return [p.text.strip() for p in prices]

    def get_cart_item_quantities(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_PAGE_PRODUCTS)
        )
        quantities = self.driver.find_elements(*self.PRODUCT_QUANTITY_IN_CART)
        return [q.text.strip() for q in quantities]
