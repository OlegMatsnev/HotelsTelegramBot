from bot.hotels_site_API.utils.requests.city_id_request.city_handler import CityApiInterface
from bot.settings import LocationSearchSiteSettings

# Создание объекта для работы с настройками сайта и API
site = LocationSearchSiteSettings()

# URL-адрес для выполнения запроса к API для поиска идентификаторов городов
url = "https://hotels4.p.rapidapi.com/locations/v3/search"

# Заголовки для запроса к API, включая ключи и хост
headers = {
    "X-RapidAPI-Key": site.api_key.get_secret_value(),
    "X-RapidAPI-Host": site.api_host
}

# Создание объекта интерфейса для работы с API городов
site = CityApiInterface()



