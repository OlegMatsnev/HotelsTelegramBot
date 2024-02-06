import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import SecretStr, StrictStr

load_dotenv()   # Загрузка переменных окружения из файла .env

"""Файл для хранения секретных данных (api keys and api hosts)"""


class PropertiesSiteSettings(BaseSettings):

    """
        Класс для хранения настроек доступа к API для сайта с Properties(hotels).
        Использует библиотеку pydantic для создания настроек с валидацией.
    """

    # Секретный ключ для доступа к API
    api_key: SecretStr = os.getenv('properties_site_API_Key', None)
    # Адрес хоста для API
    api_host: StrictStr = os.getenv('properties_site_API_Host', None)


class LocationSearchSiteSettings(BaseSettings):

    """
        Класс для хранения настроек доступа к API для сайта Location Search.
        Использует библиотеку pydantic для создания настроек с валидацией.
    """

    # Секретный ключ для доступа к API
    api_key: SecretStr = os.getenv('location_search_site_API_Key', None)
    # Адрес хоста для API
    api_host: StrictStr = os.getenv('location_search_site_API_Host', None)
