import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class CartPage:
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
        products = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.PRODUCT_ITEM)
        )
        
        for product in products:
            try:
                product_text = product.text.lower()
                
                if product_name.lower() in product_text:
                    self.actions.move_to_element(product).perform()
                    
                    time.sleep(0.5)
                    
                    try:
                        add_button = product.find_element(*self.ADD_TO_CART_BUTTON)
                    except:
                        try:
                            overlay = product.find_element(By.CSS_SELECTOR, ".overlay-content, .overlay")
                            add_button = overlay.find_element(*self.ADD_TO_CART_BUTTON)
                        except:
                            add_button = self.driver.find_element(By.XPATH, f"//a[contains(@class, 'add-to-cart') and contains(., '{product_name}')]")
                    
                    self.driver.execute_script("arguments[0].click();", add_button)
                    return True
            except Exception as e:
                continue
        
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
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cartModal"))
            )
            view_cart_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.VIEW_CART_LINK)
            )
            self.driver.execute_script("arguments[0].click();", view_cart_link)
        except:
            view_cart_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.VIEW_CART_LINK)
            )
            view_cart_link.click()

    def continue_shopping(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cartModal, .modal"))
            )
            try:
                continue_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
                )
                self.driver.execute_script("arguments[0].click();", continue_button)
            except:
                close_button = self.driver.find_element(By.CSS_SELECTOR, "button.close, .modal-header button")
                self.driver.execute_script("arguments[0].click();", close_button)
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
