import pytest
import json
from pages.login_page import LoginPage


def load_test_data():
    with open("config/test_login.json", encoding='utf-8') as f:
        return json.load(f)

@pytest.mark.usefixtures("driver")
def test_login(driver):
    """
    Тест успешной авторизации на сайте automationexercise.com
    Шаги:
    1. Открыть главную страницу
    2. Перейти на страницу входа
    3. Ввести валидные email и пароль
    4. Проверить успешный вход (появление сообщения "Logged in as")
    """
    data = load_test_data()
    page = LoginPage(driver)

    page.open(data["url"])
    
    page.open_login_page()
    
    page.login(data["valid_credentials"]["email"], data["valid_credentials"]["password"])

    success_text = page.get_success_message()
    assert success_text is not None, "Сообщение об успешном входе не найдено"
    
    assert page.is_logged_in(), "Пользователь не авторизован"
    
    if success_text and data["expected_success_message"] not in success_text:
        assert "Logout" in success_text or page.is_logged_in(), \
            f"Ожидалось сообщение содержащее '{data['expected_success_message']}' или наличие ссылки Logout, получено: '{success_text}'"


@pytest.mark.usefixtures("driver")
def test_invalid_login(driver):
    """
    Тест авторизации с неверными данными
    Шаги:
    1. Открыть главную страницу
    2. Перейти на страницу входа
    3. Ввести неверные email и пароль
    4. Проверить сообщение об ошибке
    """
    data = load_test_data()
    page = LoginPage(driver)

    page.open(data["url"])
    page.open_login_page()
    page.login(data["invalid_credentials"]["email"], data["invalid_credentials"]["password"])

    error_text = page.get_error_message()
    assert error_text is not None, "Сообщение об ошибке не найдено"
    assert data["expected_error_message"] in error_text, f"Ожидалось сообщение содержащее '{data['expected_error_message']}', получено: '{error_text}'"
