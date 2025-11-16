import pytest
import json
from pages.cart_page import CartPage

def load_test_data():
    with open("config/test_addToCart.json", encoding='utf-8') as f:
        return json.load(f)

@pytest.mark.usefixtures("driver")
def test_add_single_product_to_cart_and_verify(driver):
    """
    Тест добавления одного товара в корзину
    Шаги:
    1. Открыть страницу продуктов
    2. Добавить товар в корзину
    3. Проверить сообщение о добавлении
    4. Перейти в корзину
    5. Проверить наличие товара в корзине
    """
    data = load_test_data()
    cart_page = CartPage(driver)

    cart_page.open(data["url"])
    cart_page.open_products_page()

    product_added = cart_page.add_product_to_cart_by_name(data["first_product"]["name"])
    assert product_added, f"Товар '{data['first_product']['name']}' не найден на странице"

    cart_page.wait_for_cart_modal()
    modal_message = cart_page.get_cart_modal_message()
    assert modal_message is not None, "Модальное окно с сообщением не появилось"
    assert data["expected_cart_message"] in modal_message, f"Ожидалось сообщение '{data['expected_cart_message']}', получено: '{modal_message}'"

    cart_page.go_to_cart()

    cart_item_names = cart_page.get_cart_item_names()
    assert len(cart_item_names) > 0, "Корзина пуста"
    assert data["first_product"]["name"] in cart_item_names, f"Товар '{data['first_product']['name']}' не найден в корзине"

    cart_item_prices = cart_page.get_cart_item_prices()
    assert len(cart_item_prices) > 0, "Цены товаров не найдены"
    price_found = any(data["first_product"]["price"] in price for price in cart_item_prices)
    assert price_found, f"Цена '{data['first_product']['price']}' не найдена в корзине"


@pytest.mark.usefixtures("driver")
def test_add_multiple_products_to_cart(driver):
    """
    Тест добавления нескольких товаров в корзину
    Шаги:
    1. Открыть страницу продуктов
    2. Добавить первый товар в корзину
    3. Продолжить покупки
    4. Добавить второй товар в корзину
    5. Перейти в корзину
    6. Проверить наличие обоих товаров в корзине
    """
    data = load_test_data()
    cart_page = CartPage(driver)

    cart_page.open(data["url"])
    cart_page.open_products_page()

    product_added = cart_page.add_product_to_cart_by_name(data["first_product"]["name"])
    assert product_added, f"Товар '{data['first_product']['name']}' не найден"
    cart_page.wait_for_cart_modal()

    cart_page.continue_shopping()

    product_added = cart_page.add_product_to_cart_by_name(data["second_product"]["name"])
    assert product_added, f"Товар '{data['second_product']['name']}' не найден"
    cart_page.wait_for_cart_modal()

    cart_page.go_to_cart()

    cart_item_names = cart_page.get_cart_item_names()
    assert len(cart_item_names) >= 2, f"Ожидалось минимум 2 товара, найдено: {len(cart_item_names)}"
    assert data["first_product"]["name"] in cart_item_names, f"Первый товар '{data['first_product']['name']}' не найден"
    assert data["second_product"]["name"] in cart_item_names, f"Второй товар '{data['second_product']['name']}' не найден"
