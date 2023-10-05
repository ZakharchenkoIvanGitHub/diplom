import pytest

from testpage import OperationsHelper
import json_parser
import logging
import yaml


class SharedObject(object):
    _data = {}

    @classmethod
    def set(cls, **kw):
        cls._data.update(kw)

    @classmethod
    def get(cls, key):
        return cls._data.get(key)


class TestYandexWeather:
    with open("testdata.yaml", encoding="utf-8") as f:
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
        weather_data = test_page.get_data_weather(SharedObject.get("lat"), SharedObject.get("lon"))
        SharedObject.set(weather_data=weather_data)
        assert weather_data

    @pytest.mark.skip()
    def test_step3(self, browser):
        """
        Тест проверяет, что данные о городе полученные с помощью сервиса API Яндекс.Погоды,
        соответствуют данным на странице
        """
        logging.info("Test_3 Starting")
        test_page = OperationsHelper(browser)
        city_name = test_page.get_city_name(self.testdata["city"])
        assert city_name == json_parser.get_city(SharedObject.get("weather_data"))

    @pytest.mark.skip()
    def test_step4(self, browser):
        """
        Проверка соответствия текущей температуры
        """
        logging.info("Test_4 Starting")
        test_page = OperationsHelper(browser)
        fact_temp = test_page.get_fact_temp()
        assert fact_temp == json_parser.get_fact_temp(SharedObject.get("weather_data"))

    @pytest.mark.skip()
    def test_step5(self, browser):
        """
        Проверка соответствия ощущаемой температуры
        """
        logging.info("Test_5 Starting")
        test_page = OperationsHelper(browser)
        feels_like = test_page.get_feels_like()
        assert feels_like == json_parser.get_feels_like(SharedObject.get("weather_data"))

    @pytest.mark.skip()
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
