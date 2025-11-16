"""
Тесты для проверки функциональности оформления заказа.

Содержит тесты:
- Оформление заказа авторизованным пользователем
- Полный процесс: авторизация -> добавление товара -> оформление -> оплата
"""

import pytest
import json
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.order_page import OrderPage

def load_test_data():
    """
    Загружает тестовые данные из JSON конфигурационного файла.
    
    Returns:
        dict: Словарь с тестовыми данными (URL, товары, учетные данные, данные заказа)
    """
    with open("config/test_makeOrder.json", encoding='utf-8') as f:
        return json.load(f)

@pytest.mark.usefixtures("driver")
def test_make_order_with_auth_user(driver):
    """
    Тест оформления заказа авторизованным пользователем
    Шаги:
    1. Авторизоваться на сайте
    2. Добавить товар в корзину
    3. Перейти в корзину
    4. Оформить заказ
    5. Заполнить данные платежа
    6. Подтвердить заказ
    7. Проверить успешное оформление заказа
    """
    data = load_test_data()
    login_page = LoginPage(driver)
    cart_page = CartPage(driver)
    order_page = OrderPage(driver)

    # Шаг 1: Авторизация
    login_page.open(data["url"])
    login_page.open_login_page()
    login_page.login(data["valid_credentials"]["email"], data["valid_credentials"]["password"])
    assert login_page.is_logged_in(), "Пользователь не авторизован"

    # Шаг 2: Добавить товар в корзину
    cart_page.open_products_page()
    product_added = cart_page.add_product_to_cart_by_name(data["product"]["name"])
    assert product_added, f"Товар '{data['product']['name']}' не найден"
    cart_page.wait_for_cart_modal()
    cart_page.go_to_cart()

    # Шаг 3: Перейти к оформлению заказа
    order_page.proceed_to_checkout()

    # Шаг 4: Оформить заказ
    order_page.place_order()

    # Шаг 5: Заполнить данные платежа
    card_data = {
        "name": data["order_data"]["name"],
        "card_number": "1234567890123456",
        "cvc": "123",
        "expiry_month": "12",
        "expiry_year": "2025"
    }
    order_page.fill_payment_form(card_data)

    # Шаг 6: Подтвердить платеж
    order_page.submit_payment()

    # Шаг 7: Проверить успешное оформление заказа
    success_message = order_page.get_success_message()
    assert success_message is not None, "Сообщение об успешном заказе не найдено"
    # Проверка нечувствительна к регистру, так как на сайте может быть "ORDER PLACED!" или "Order Placed!"
    assert data["expected_success_message"].upper() in success_message.upper(), \
        f"Ожидалось сообщение '{data['expected_success_message']}', получено: '{success_message}'"
    
    # Дополнительная проверка
    assert order_page.is_order_placed(), "Заказ не был оформлен"