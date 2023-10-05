import json


def get_city(json_data):
    return json_data["geo_object"]["locality"]["name"]


def get_fact_temp(json_data):
    return str(json_data["fact"]["temp"])


def get_feels_like(json_data):
    return str(json_data["fact"]["feels_like"])


def get_icon_src(json_data):
    return f'https://yastatic.net/weather/i/icons/confident/light/svg/{str(json_data["fact"]["icon"])}.svg'

def get_condition(json_data):
    condition = str(json_data["fact"]["condition"])
    match condition:
        case "clear":
            return "Ясно"
        case"partly-cloudy":
            return "Малооблачно"
        case "cloudy":
            return "Облачно с прояснениями"
        case"overcast":
            return "Пасмурно"
        case "light-rain":
            return "Небольшой дождь"
        case"rain":
            return "Дождь"
        case "heavy-rain":
            return "Сильный дождь"
        case"showers":
            return "Ливень"
        case"wet-snow":
            return "Дождь со снегом"
        case"light-snow":
            return "Небольшой снег"
        case"snow":
            return "Снег"
        case"snow-showers":
            return "Снегопад"
        case"hail":
            return "Град"
        case"thunderstorm":
            return "Гроза"
        case"thunderstorm-with-rain":
            return "Дождь с грозой"
        case"thunderstorm-with-hail":
            return "Гроза с градом"


if __name__ == "__main__":
    with open('1.json', 'r', encoding='utf-8') as f:
        text = json.load(f)

    print(get_city(text))
