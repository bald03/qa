import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    
    SUCCESS_MESSAGE = (By.XPATH, "//li/a[contains(@href, '/logout')] | //a[contains(@href, '/logout')]")
    
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p[style*='color: red'], .login-form p")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(base_url)

    def open_login_page(self):
        login_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_LINK)
        )
        login_link.click()

    def login(self, email, password):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(email)
        
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
        
        time.sleep(2)

    def get_success_message(self):
        try:
            success_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)
            )
            
            try:
                parent = success_element.find_element(By.XPATH, "./..")
                parent_text = parent.text.strip()
                if "Logged in as" in parent_text:
                    return parent_text
            except:
                pass
            
            try:
                li_element = success_element.find_element(By.XPATH, "./ancestor::li[1]")
                li_text = li_element.text.strip()
                if "Logged in as" in li_text:
                    return li_text
            except:
                pass
            
            return success_element.text.strip()
        except:
            try:
                logged_in_text = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Logged in as')] | //a[contains(@href, '/logout')]/ancestor::li[1]"))
                )
                return logged_in_text.text.strip()
            except:
                return None

    def get_error_message(self):
        try:
            # Ожидаем появления видимого элемента с ошибкой (до 5 секунд)
            error_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text.strip()
        except:
            return None

    def is_logged_in(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/logout')] | //li[contains(text(), 'Logged in as')]"))
                )
                return True
            except:
                return False
