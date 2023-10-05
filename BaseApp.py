import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://yandex.ru/pogoda/"

    def find_element(self, locator, time=10):
        try:
            element = WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                             message=f"Element not found {locator}")
        except:
            logging.exception("Find element exception")
            element = None
        return element

    def get_element_property(self, mode, locator, property):
        element = self.find_element(mode, locator)
        if element:
            return element.value_of_css_property(property)
        else:
            logging.error(f"Property {property} not found no element with locator {locator}")
            return None

    def go_to_site(self):
        try:
            start_browsing = self.driver.get(self.base_url)
        except:
            logging.exception("Exception while open site")
            start_browsing = None
        return start_browsing

    def get_alert(self, time=10):
        try:
            alert = WebDriverWait(self.driver, time).until(EC.alert_is_present(),
                                                           message=f"alert ot found")
            return alert
        except:
            logging.exception("Exception with alert")
            return None
