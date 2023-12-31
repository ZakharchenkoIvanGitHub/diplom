import json


def get_city(json_data):
    """
    Возвращает название города
    """
    return json_data["geo_object"]["locality"]["name"]


def get_fact_temp(json_data):
    """
    Возвращает текущую температуру
    """
    return get_temp(json_data["fact"]["temp"])


def get_feels_like(json_data):
    """
    Возвращает ощущаемую температуру
    """
    return get_temp(json_data["fact"]["feels_like"])


def get_temp(temp):
    if temp > 0:
        temp = f"+{temp}"
    elif temp < 0:
        temp = f"−{str(temp)[1:]}"
    else:
        temp = f"{temp}"
    return temp


def get_icon_src(json_data):
    """
    Возвращает адрес иконки
    """
    return f'https://yastatic.net/weather/i/icons/confident/light/svg/{json_data["fact"]["icon"]}.svg'


def get_condition(json_data):
    """
    Возвращает описание погоды
    """
    condition = json_data["fact"]["condition"]
    match condition:
        case "clear":
            return "Ясно"
        case "partly-cloudy":
            return "Малооблачно"
        case "cloudy":
            return "Облачно с прояснениями"
        case "overcast":
            return "Пасмурно"
        case "light-rain":
            return "Небольшой дождь"
        case "rain":
            return "Дождь"
        case "heavy-rain":
            return "Сильный дождь"
        case "showers":
            return "Ливень"
        case "wet-snow":
            return "Дождь со снегом"
        case "light-snow":
            return "Небольшой снег"
        case "snow":
            return "Снег"
        case "snow-showers":
            return "Снегопад"
        case "hail":
            return "Град"
        case "thunderstorm":
            return "Гроза"
        case "thunderstorm-with-rain":
            return "Дождь с грозой"
        case "thunderstorm-with-hail":
            return "Гроза с градом"


def get_yesterday_temp(json_data):
    """
    Возвращает температуру вчера в это время
    """
    return str(json_data["yesterday"]["temp"])


def get_wind_speed(json_data):
    """
    Возвращает скорость ветра
    """
    return str(float(json_data["fact"]["wind_speed"])).replace('.', ',')


def get_wind_dir(json_data):
    """
    Возвращает направление ветра
    """
    wind_dir = json_data["fact"]["wind_dir"]
    match wind_dir:
        case "nw":
            return "СЗ"
        case "n":
            return "С"
        case "ne":
            return "СВ"
        case "e":
            return "В"
        case "se":
            return "ЮВ"
        case "s":
            return "Ю"
        case "sw":
            return "ЮЗ"
        case "w":
            return "З"
        case "c":
            return "Ш"


def get_humidity(json_data):
    """
    Возвращает влажность
    """
    return str(json_data["fact"]["humidity"])


def get_pressure(json_data):
    """
    Возвращает атмосферное давление
    """
    return str(json_data["fact"]["pressure_mm"])


if __name__ == "__main__":
    with open('1.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
