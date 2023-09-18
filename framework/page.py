from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Page:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((by, value))
        )

    def click_element(self, element):
        element.click()

    def send_keys_to_element(self, element, keys):
        element.clear()
        element.send_keys(keys)

    def reset_app(self):
        self.driver.reset()
