from BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import logging
import yaml


class TestSearchLocators:
    ids = dict()
    with open("locators.yaml", encoding="utf-8") as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])


#    for locator in locators["css"].keys():
#        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])

class OperationsHelper(BasePage):
    with open("testdata.yaml", encoding="utf-8") as f:
        testdata = yaml.safe_load(f)

    @staticmethod
    def input_city_to_xpath(locator, city):
        ind = locator[1].find("''")
        xpath = f"{locator[1][:ind + 1]}{city}{locator[1][ind + 1:]}"
        return locator[0], xpath

    @staticmethod
    def get_lat_lon(url):
        ind = url.find("lat")
        lat = url[ind + 4:ind + 15]
        ind = url.find("lon")
        lon = url[ind + 4:ind + 15]
        return lat, lon

    @staticmethod
    def get_city_name(full_name):
        ind = full_name.find(",")
        name = full_name[:ind] if ind != -1 else full_name
        return name

    def enter_text_info_field(self, locator, word, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f"Send {word} to element {element_name}")
        field = self.find_element(locator)
        if not field:
            logging.error(f"Element {locator} not found")
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f"Exception while operation with {locator}")

    def click_button(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception("Exception witch click")
        logging.debug(f"Click to element {element_name} button")
        return True

    def get_text_from_element(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f"Exception while get text from {element_name}")
            return None
        logging.debug(f"Find text {text} in field {element_name}")
        return text

    def get_attribute_from_element(self, locator, attribute, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            attr = field.get_attribute(attribute)
        except:
            logging.exception(f"Exception while get text from {element_name}")
            return None
        logging.debug(f"Find attribute {attribute} in field {element_name}")
        return attr

    # ENTER TEXT
    def enter_city(self, word):
        self.enter_text_info_field(TestSearchLocators.ids["LOCATOR_INPUT_CITY"], word, description="INPUT_LOGIN")

    #
    #    def enter_pass(self, word):
    #        self.enter_text_info_field(TestSearchLocators.ids["LOCATOR_INPUT_PASSWORD"], word, description="INPUT_PASSWORD")
    #
    #    def enter_name(self, word):
    #        self.enter_text_info_field(TestSearchLocators.ids["LOCATOR_DESCRIPTION_NAME"], word, description="INPUT_NAME")
    #
    #    def enter_email(self, word):
    #        self.enter_text_info_field(TestSearchLocators.ids["LOCATOR_DESCRIPTION_EMAIL"], word, description="INPUT_EMAIL")
    #
    #    def enter_content(self, word):
    #        self.enter_text_info_field(TestSearchLocators.ids["LOCATOR_CONTENT_CREATE"], word, description="INPUT_CREATE")

    # CLICK
    def press_enter_city(self):
        self.find_element(TestSearchLocators.ids["LOCATOR_INPUT_CITY"]).send_keys(Keys.ENTER)

    def click_city(self, city):
        self.click_button(self.input_city_to_xpath(TestSearchLocators.ids['LOCATOR_LINK_TEXT'], city),
                          description="click_city")

    #
    #    def click_input_file(self):
    #        self.click_button(TestSearchLocators.ids["LOCATOR_INPUT_FILE"], description="input file")
    #
    #    def click_contact(self):
    #        self.click_button(TestSearchLocators.ids["LOCATOR_CONTACT"], description="contact")
    #
    #    def click_button_contact_as(self):
    #        self.click_button(TestSearchLocators.ids["LOCATOR_BUTTON"], description="contact as")

    # GET TEXT
    def get_city_title(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_CITY_TITLE"], description="city_title")

    def get_fact_temp(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_FACT_TEMP"], description="fact_temp")[1:]

    def get_feels_like(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_FEELS_LIKE"], description="feels_like")[1:]

    def get_icon_src(self):
        return self.get_attribute_from_element(TestSearchLocators.ids["LOCATOR_ICON"], 'src', description="icon_src")

    def get_condition(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_CONDITION"], description="condition")
    #    def go_alert(self):
    #        logging.info("Go_alert")
    #        alert = self.get_alert()
    #        text = alert.text
    #        logging.info(f"Alert text '{text}'")
    #        alert.accept()
    #        return text

    def get_data_weather(self, lat, lon):
        """
        Получает данные о погоде используя API сервис Яндекс
        :param lat: <широта>
        :param lon:<долгота>
        :return: данные о погоде в формате json
        """
        params = {"lat": lat,
                  "lon": lon,
                  "extra": self.testdata["extra"],
                  "lang": self.testdata["lang"],
                  "limit": self.testdata["limit"],
                  "hours": self.testdata["hours"]}

        response = requests.get("https://api.weather.yandex.ru/v2/forecast?",
                                headers={"X-Yandex-API-Key": self.testdata["token"]},
                                params=params)
        if response.status_code == 200:
            logging.debug(f"Данные о погоде получены")
            return response.json()
        elif response.status_code == 403:
            logging.error(f"Превышение суточного лимита запросов, status_code {response.status_code}")
        elif response.status_code == 404:
            logging.error(f"Параметры заданы некорректно, status_code {response.status_code}")
        else:
            logging.error(f"Данные о погоде не получены, status_code {response.status_code}")
