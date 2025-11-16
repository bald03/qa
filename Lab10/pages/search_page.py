from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:

    SEARCH_INPUT = (By.CSS_SELECTOR, "input#search_product, input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button#submit_search, button[type='submit']")
    SEARCH_RESULTS_TITLE = (By.CSS_SELECTOR, "h2.title.text-center, h2.text-center")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".productinfo, .single-products")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(base_url)

    def search(self, query):
        try:
            search_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
        except:
            products_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/products']")
            products_link.click()
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )

        search_input.clear()
        search_input.send_keys(query)

        search_button = self.driver.find_element(*self.SEARCH_BUTTON)
        search_button.click()

    def get_search_results_title(self):
        try:
            title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SEARCH_RESULTS_TITLE)
            )
            return title_element.text.strip()
        except:
            return None

    def get_search_results_count(self):
        try:
            products = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.PRODUCT_ITEMS)
            )
            return len(products)
        except:
            return 0

    def has_search_results(self):
        return self.get_search_results_count() > 0
