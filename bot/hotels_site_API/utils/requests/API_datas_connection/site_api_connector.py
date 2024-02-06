from bot.hotels_site_API.utils.requests.API_datas_connection.site_API_handler import SiteApiInterface
from bot.settings import PropertiesSiteSettings

# Создание объекта для работы с настройками сайта и API
site = PropertiesSiteSettings()

# URL и заголовки для выполнения запросов к API
url = "https://hotels4.p.rapidapi.com/properties/v2/list"
headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": site.api_key.get_secret_value(),
        "X-RapidAPI-Host": site.api_host
    }

# Создание объекта интерфейса для работы с API сайта
site_api = SiteApiInterface()

