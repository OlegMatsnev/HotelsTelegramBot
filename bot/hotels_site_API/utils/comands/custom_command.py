from bot.hotels_site_API.utils.requests.API_datas_connection.site_api_connector import url, headers, site_api
from bot.hotels_site_API.utils.hotel import Hotel

get_hotels = site_api.get_hotels()


def get_price() -> (int, int):

    """
    Запрашивает и возвращает минимальную и максимальную цену для отелей.

    Returns:
        Tuple[int, int]: Кортеж с минимальной и максимальной ценой в долларах.
    """

    min_price = 0
    max_price = 5000

    while True:
        try:
            min_price = int(input('Введите минимально допустимую цену в долларах (не ниже 0 и не больше 800):'))
            if not (0 <= min_price <= 800):
                continue
            else:
                break
        except (TypeError, ValueError):
            print('Ошибка! Введите сумму от 0$ до 800$.')
            continue

    while True:
        try:
            max_price = int(input(f'Введите максимально допустимую цену в долларах (не ниже {min_price}$):'))
            if max_price <= min_price:
                print('Максимально допустимая цена не может быть ниже или равной минимальной!')
                continue
            else:
                break
        except (TypeError, ValueError):
            print(f'Ошибка! Введите сумму больше {min_price}$.')
            continue

    return min_price, max_price


def get_stars() -> str:

    """
    Запрашивает и возвращает количество звёзд для отелей.

    Returns:
        str: Количество звёзд в виде строки (значения от 30 до 50).
    """

    stars = 4

    while True:
        try:
            stars = int(input('Введите количество звёзд у запрашиваемых отелей (число от 3 до 5):'))
            if not (3 <= stars <= 5):
                print('Число должно быть от 3 до 5.')
                continue
            else:
                break
        except (TypeError, ValueError):
            print('Ошибка! Введите число от 3 до 5.')
            continue

    return str(stars * 10)


def prices_compliance_checking_hotels(hotels: list[Hotel], min_price: int, max_price: int) -> list[Hotel]:
    """
     Функция для повторной проверки отелей на соответствие ценовому диапазону пользователя.

     Args:
         hotels (list[Hotel]): Список объектов типа Hotel.
         min_price (int): Минимальная цена в долларах.
         max_price (int): Максимальная цена в долларах.

     Returns:
         list[Hotel]: Отфильтрованный список отелей.
     """

    new_list: list[Hotel] = []

    for hotel in hotels:
        if min_price <= hotel.price_per_night <= max_price:
            new_list.append(hotel)

    return new_list


def custom(data_list: list, count_hotels=5, price_filter=False, stars_filter=False, pool_filter=False):
    """
        Основная функция для выбора отелей на основе пользовательских критериев.

        Args:
            data_list (list): Список данных о поиске (например, дата приезда, дата отъезда, комнаты и город).
            count_hotels (int): Количество отелей для выбора.
            price_filter (bool): Фильтровать ли по цене.
            stars_filter (bool): Фильтровать ли по количеству звёзд.
            pool_filter (bool): Фильтровать ли по наличию бассейна.

        Ex:
            {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {
        "regionId": "6054439"
    },
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2022
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2022
    },
    "rooms": [
        {
            "adults": 2,
            "children": [
                {
                    "age": 5
                },
                {
                    "age": 7
                }
            ]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {
        "price": {
            "max": 150,
            "min": 100
        },
        "guestRating": "35",
        "star": ["40","50"]
    }
}

        Returns:
            list[Hotel]: Список выбранных отелей.
        """

    if price_filter:
        min_price, max_price = get_price()
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
                                     filters={"price": {"max": max_price, "min": min_price}})

        result_list = prices_compliance_checking_hotels(all_city_hotels, min_price=min_price, max_price=max_price)

        return result_list[:count_hotels]

    if stars_filter:
        stars_hotel_count = get_stars()
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
                                     filters={"star": [stars_hotel_count]})
        return all_city_hotels[:count_hotels]

    if pool_filter:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
                                     filters={"amenities": ["POOL"]})
        return all_city_hotels[:count_hotels]
