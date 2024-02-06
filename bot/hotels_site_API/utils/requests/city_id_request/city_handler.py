import requests
from typing import Dict
import json

cache_file_path = "C:\\Users\\User\\PycharmProjects\\TelegramBot\\bot\\hotels_site_API\\utils\\requests" \
             "\\city_id_request\\cities_id_file.json"
CACHE_FILE = cache_file_path    # Путь к файлу для кэширования данных о городах
cache = {}                      # Словарь для хранения кэшированных данных


def _make_request(url: str, headers: Dict, params: Dict, success=200):

    # Выполнение GET-запроса к API с указанными параметрами и заголовками
    response = requests.get(url=url, headers=headers, params=params)
    response_status = response.status_code

    # Если статус ответа соответствует успешному запросу, возвращаем сам ответ
    if response_status == success:
        return response

    # Возвращаем статус ответа
    return response_status


def _get_city_id(url: str, headers: Dict, city_name: str, func=_make_request) -> (int, None):
    # Функция для чтения кэшированных данных из файла
    def read_cache_datas() -> None:

        try:
            with open(CACHE_FILE, 'r') as file:
                cache.update(json.load(file))
        except FileNotFoundError:
            with open(CACHE_FILE, "w") as file:
                file.write("")

    # Функция для сохранения данных в кэше
    def save_datas(town, town_id) -> None:
        cache[town] = town_id

        with open(CACHE_FILE, 'w') as file:
            json.dump(cache, file, indent=4)

    read_cache_datas()          # Чтение кэшированных данных

    # Если название города уже находится в кэше, возвращаем его идентификатор
    if city_name in cache:
        return cache[city_name]

    # Параметры запроса к API для поиска идентификатора города
    querystring = {"q": city_name, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    # Выполнение GET-запроса к API
    response = func(url=url, headers=headers, params=querystring)

    # Парсинг JSON-ответа
    response_js = response.json()
    try:
        # Извлечение идентификатора города из ответа и сохранение его в кэше
        save_id = response_js['sr'][0]['gaiaId']
        save_datas(city_name, save_id)
        return save_id
    except KeyError:
        print('Некорректный ключ')


class CityApiInterface:

    @staticmethod
    def get_city_id():
        return _get_city_id


CityApiInterface()  # Создание объекта интерфейса для работы с API городов
