from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CategoryPage:
    MENU_MEN = (By.CSS_SELECTOR, "ul.menu > li > a[href='category/men']")
    SUBMENU_ELEKTRONNYE = (By.CSS_SELECTOR, "ul li ul li > a[href='category/elektronnye']")
    SUBMENU_CASIO = (By.CSS_SELECTOR, "ul li ul li ul li > a[href='category/casio']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "div.product-bottom > h3")

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)

    def open(self, base_url):
        self.driver.get(base_url)

    def go_to_category(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.MENU_MEN))
        self.actions.move_to_element(self.driver.find_element(*self.MENU_MEN)).perform()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.SUBMENU_ELEKTRONNYE))
        self.actions.move_to_element(self.driver.find_element(*self.SUBMENU_ELEKTRONNYE)).perform()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SUBMENU_CASIO)).click()

    def get_product_titles(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.PRODUCT_NAMES))
        return [el.text.strip() for el in self.driver.find_elements(*self.PRODUCT_NAMES)]
