from testpage import OperationsHelper
import json_parser
import logging
import yaml
from weather_api import get_data_weather


class SharedObject(object):
    _data = {}

    @classmethod
    def set(cls, **kw):
        cls._data.update(kw)

    @classmethod
    def get(cls, key):
        return cls._data.get(key)


class TestYandexWeather:
    with open("config.yaml", encoding="utf-8") as f:
        testdata = yaml.safe_load(f)

    def test_step1(self, browser):
        """
        Тест открывает главную страницу "Яндекс погода",
        вводит название города,
        подтверждает название на дополнительной странице,
        получает координаты города,
        проверяет, что открылась страница с искомым городом
        """
        logging.info("Test_1 Starting")
        test_page = OperationsHelper(browser)
        test_page.go_to_site()
        test_page.enter_city(self.testdata["city"])
        test_page.press_enter_city()
        test_page.click_city(self.testdata["city"])
        lat, lon = test_page.get_lat_lon(browser.current_url)
        SharedObject.set(lat=lat)
        SharedObject.set(lon=lon)
        city_name = test_page.get_city_name(self.testdata["city"])
        assert city_name == test_page.get_city_title()

    def test_step2(self, browser):
        """
        Тест получает данные о погоде с помощью сервиса API Яндекс.Погоды,
        проверяет, что данные получены.
        """
        logging.info("Test_2 Starting")
        test_page = OperationsHelper(browser)
        weather_data = get_data_weather(SharedObject.get("lat"), SharedObject.get("lon"))
        SharedObject.set(weather_data=weather_data)
        assert weather_data

    def test_step3(self, browser):
        """
        Тест проверяет, что данные о городе полученные с помощью сервиса API Яндекс.Погоды,
        соответствуют данным на странице
        """
        logging.info("Test_3 Starting")
        test_page = OperationsHelper(browser)
        city_name = test_page.get_city_name(self.testdata["city"])
        assert city_name == json_parser.get_city(SharedObject.get("weather_data"))

    def test_step4(self, browser):
        """
        Проверка соответствия текущей температуры
        """
        logging.info("Test_4 Starting")
        test_page = OperationsHelper(browser)
        fact_temp = test_page.get_fact_temp()
        assert fact_temp == json_parser.get_fact_temp(SharedObject.get("weather_data"))

    def test_step5(self, browser):
        """
        Проверка соответствия ощущаемой температуры
        """
        logging.info("Test_5 Starting")
        test_page = OperationsHelper(browser)
        feels_like = test_page.get_feels_like()
        assert feels_like == json_parser.get_feels_like(SharedObject.get("weather_data"))

    def test_step6(self, browser):
        """
        Проверка соответствия иконки погоды
        """
        logging.info("Test_6 Starting")
        test_page = OperationsHelper(browser)
        icon_src = test_page.get_icon_src()
        assert icon_src == json_parser.get_icon_src(SharedObject.get("weather_data"))

    def test_step7(self, browser):
        """
        Проверка соответствия погодного описания
        """
        logging.info("Test_7 Starting")
        test_page = OperationsHelper(browser)
        condition = test_page.get_condition()
        assert condition == json_parser.get_condition(SharedObject.get("weather_data"))

    def test_step8(self, browser):
        """
        Проверка соответствия температуры вчера в это время
        """
        logging.info("Test_8 Starting")
        test_page = OperationsHelper(browser)
        yesterday_temp = test_page.get_yesterday_temp()
        assert yesterday_temp == json_parser.get_yesterday_temp(SharedObject.get("weather_data"))

    def test_step9(self, browser):
        """
        Проверка соответствия скорости ветра
        """
        logging.info("Test_9 Starting")
        test_page = OperationsHelper(browser)
        wind_speed = test_page.get_wind_speed()
        assert wind_speed == json_parser.get_wind_speed(SharedObject.get("weather_data"))

    def test_step10(self, browser):
        """
        Проверка соответствия направления ветра
        """
        logging.info("Test_10 Starting")
        test_page = OperationsHelper(browser)
        wind_dir = test_page.get_wind_dir()
        assert wind_dir == json_parser.get_wind_dir(SharedObject.get("weather_data"))

    def test_step11(self, browser):
        """
        Проверка соответствия влажности
        """
        logging.info("Test_11 Starting")
        test_page = OperationsHelper(browser)
        humidity = test_page.get_humidity()
        assert humidity == json_parser.get_humidity(SharedObject.get("weather_data"))

    def test_step12(self, browser):
        """
        Проверка соответствия давления
        """
        logging.info("Test_12 Starting")
        test_page = OperationsHelper(browser)
        pressure = test_page.get_pressure()
        assert pressure == json_parser.get_pressure(SharedObject.get("weather_data"))
