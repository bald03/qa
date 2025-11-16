import pytest
import json
from pages.search_page import SearchPage

def load_test_data():

    with open("config/test_search.json", encoding='utf-8') as f:
        return json.load(f)

@pytest.mark.usefixtures("driver")
def test_search_with_query(driver):
    """
    Тест поиска товаров по запросу
    Шаги:
    1. Открыть главную страницу
    2. Выполнить поиск по запросу
    3. Проверить заголовок результатов поиска
    4. Проверить наличие результатов поиска
    """
    data = load_test_data()
    page = SearchPage(driver)

    page.open(data["url"])

    page.search(data["valid_query"])

    search_results_title = page.get_search_results_title()
    assert search_results_title is not None, "Заголовок результатов поиска не найден"
    assert data["expected_search_results_title"] in search_results_title, f"Ожидался заголовок '{data['expected_search_results_title']}', получено: '{search_results_title}'"

    assert page.has_search_results(), "Результаты поиска не найдены"

    results_count = page.get_search_results_count()
    assert results_count > 0, f"Ожидалось найти товары, найдено: {results_count}"


@pytest.mark.usefixtures("driver")
def test_search_empty_query(driver):
    """
    Тест поиска с пустым запросом
    Шаги:
    1. Открыть главную страницу
    2. Выполнить поиск с пустым запросом
    3. Проверить заголовок результатов (при пустом запросе показывается "ALL PRODUCTS")
    """
    data = load_test_data()
    page = SearchPage(driver)

    page.open(data["url"])
    page.search(data["empty_query"])

    search_results_title = page.get_search_results_title()
    assert search_results_title is not None, "Заголовок результатов поиска не найден"
    expected_title = data.get("expected_empty_search_title", "ALL PRODUCTS")
    assert expected_title in search_results_title, f"Ожидался заголовок содержащий '{expected_title}', получено: '{search_results_title}'"