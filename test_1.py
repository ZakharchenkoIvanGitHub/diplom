from testpage import OperationsHelper
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
        test_page = OperationsHelper(browser)
        weather_data = test_page.get_data_weather(SharedObject.get("lat"), SharedObject.get("lon"))
        print(weather_data)
        assert weather_data
