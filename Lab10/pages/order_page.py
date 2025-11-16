"""
Page Object класс для работы с оформлением заказа.

Этот класс инкапсулирует логику работы с процессом оформления заказа:
- Переход к оформлению заказа
- Заполнение данных платежа
- Подтверждение заказа
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class OrderPage:
    """
    Класс для работы с оформлением заказа на AutomationExercise.com.
    
    Основные функции:
    - Переход к оформлению заказа из корзины
    - Заполнение формы платежа
    - Подтверждение заказа
    - Проверка успешного оформления
    """
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//a[contains(@class, 'check_out') and contains(text(), 'Proceed To Checkout')] | //a[contains(@class, 'check_out')]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//a[contains(@class, 'check_out') and contains(text(), 'Place Order')] | //a[contains(@class, 'check_out')]")
    
    # Форма доставки
    NAME_INPUT = (By.CSS_SELECTOR, "input[name='name_on_card']")
    CARD_NUMBER_INPUT = (By.CSS_SELECTOR, "input[name='card_number']")
    CVC_INPUT = (By.CSS_SELECTOR, "input[name='cvc']")
    EXPIRY_MONTH_INPUT = (By.CSS_SELECTOR, "input[name='expiry_month']")
    EXPIRY_YEAR_INPUT = (By.CSS_SELECTOR, "input[name='expiry_year']")
    PAY_BUTTON = (By.CSS_SELECTOR, "button#submit, button[data-qa='pay-button']")
    
    # Сообщения
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "p[style*='color: green'], .alert-success")
    ORDER_PLACED_MESSAGE = (By.XPATH, "//h2[contains(text(), 'Order Placed')] | //h2[@data-qa='order-placed']")
    
    # Если требуется регистрация/логин
    SIGNUP_NAME_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    def __init__(self, driver):
        self.driver = driver

    def proceed_to_checkout(self):
        proceed_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PROCEED_TO_CHECKOUT_BUTTON)
        )
        proceed_button.click()

    def place_order(self):
        place_order_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PLACE_ORDER_BUTTON)
        )
        place_order_button.click()

    def fill_payment_form(self, card_data):
        name_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.NAME_INPUT)
        )
        name_input.send_keys(card_data.get("name", "Test User"))
        
        card_number_input = self.driver.find_element(*self.CARD_NUMBER_INPUT)
        card_number_input.send_keys(card_data.get("card_number", "1234567890123456"))
        
        cvc_input = self.driver.find_element(*self.CVC_INPUT)
        cvc_input.send_keys(card_data.get("cvc", "123"))
        
        expiry_month_input = self.driver.find_element(*self.EXPIRY_MONTH_INPUT)
        expiry_month_input.send_keys(card_data.get("expiry_month", "12"))
        
        expiry_year_input = self.driver.find_element(*self.EXPIRY_YEAR_INPUT)
        expiry_year_input.send_keys(card_data.get("expiry_year", "2025"))

    def submit_payment(self):
        pay_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PAY_BUTTON)
        )
        pay_button.click()

    def get_success_message(self):
        try:
            # Пытаемся найти сообщение об успешном заказе
            success_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.ORDER_PLACED_MESSAGE)
            )
            return success_element.text.strip()
        except:
            try:
                # Альтернативный вариант
                success_element = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
                )
                return success_element.text.strip()
            except:
                return None

    def is_order_placed(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.ORDER_PLACED_MESSAGE)
            )
            return True
        except:
            return False
