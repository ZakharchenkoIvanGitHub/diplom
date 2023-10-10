import requests
import logging
import yaml

with open("testdata.yaml", encoding="utf-8") as f:
    testdata = yaml.safe_load(f)


def get_data_weather(lat, lon):
    """
    Получает данные о погоде используя API сервис Яндекс
    :param lat: <широта>
    :param lon:<долгота>
    :return: данные о погоде в формате json
    """
    params = {"lat": lat,
              "lon": lon,
              "extra": testdata["extra"],
              "lang": testdata["lang"],
              "limit": testdata["limit"],
              "hours": testdata["hours"]}

    response = requests.get("https://api.weather.yandex.ru/v2/forecast?",
                            headers={"X-Yandex-API-Key": testdata["token"]},
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
