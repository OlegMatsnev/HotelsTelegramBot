import requests
from typing import Dict
from bot.hotels_site_API.utils.hotel import Hotel


def create_hotel_objects(hotels) -> list[Hotel]:
    """
        Функция создает объекты типа Hotel из данных об отелях.

        Args:
            hotels: Список данных об отелях.

        Returns:
            :return hotels list with the type 'Hotel'
            :rtype list[Hotel]
        """

    hotels_list = []

    for hotel_data in hotels:
        try:
            hotel_name = hotel_data['name']
            hotel_avail = hotel_data['availability']['available']
            hotel_room_left = hotel_data['availability']['minRoomsLeft']
            hotel_picture = hotel_data['propertyImage']['image']['url']
            hotel_price_per_night = hotel_data['price']['lead']['amount']
            hotel_price_total = hotel_data['price']['displayMessages'][1]['lineItems'][0]['value']
            hotel_reviews_count = hotel_data['reviews']['total']
            hotel_reviews_score = hotel_data['reviews']['score']
            hotel_destination_info = hotel_data['destinationInfo']['distanceFromDestination']['value']
            hotel_id = hotel_data['id']

            if (hotel_price_per_night and hotel_reviews_score and hotel_destination_info) is not None:
                hotel = Hotel(
                    name=hotel_name,
                    is_available=hotel_avail,
                    min_rooms_left=hotel_room_left,
                    picture_url=hotel_picture,
                    price_per_night=hotel_price_per_night,
                    total_price=hotel_price_total,
                    reviews_count=hotel_reviews_count,
                    reviews_score=hotel_reviews_score,
                    destination_info=hotel_destination_info,
                    id=hotel_id
                )

                hotels_list.append(hotel)
        except (KeyError, TypeError) as e:
            continue

    return hotels_list


def _make_request(url: str, headers: Dict,  payload: Dict, success=200):
    """
        Функция отправляет POST-запрос на указанный URL с заданными заголовками и данными.

        Args:
            url (str): URL для запроса.
            headers (Dict): Заголовки для запроса.
            payload (Dict): Данные для запроса.
            success (int): Код успешного ответа.

        Returns:
            :return hotels list
            :rtype list[Hotel] or int: ->
            -> Список объектов типа Hotel в случае успешного ответа, или код ответа в случае неудачи.
        """

    response = requests.post(url, json=payload, headers=headers)
    status_code = response.status_code

    if status_code == success:
        try:
            response_js = response.json()
            hotels = response_js['data']['propertySearch']['properties']
            hotels_list = create_hotel_objects(hotels)
            return hotels_list
        except BaseException as e:
            print('ошибка', e)

    return status_code


def _get_hotels(url: str, headers: Dict, data_list, filters=None, sort=None, func=_make_request):
    """
        Осуществляет запрос к API для получения списка отелей на основе указанных данных, фильтров и сортировки.

        Args:
            url (str): URL для запроса.
            headers (Dict): Заголовки для запроса.
            data_list: Список данных для запроса.
            filters (Dict): Фильтры для запроса (по умолчанию None).
            sort (str): Критерий сортировки (по умолчанию None).
            func: Функция для выполнения запроса (по умолчанию _make_request).

        Returns:
            :return hotels list
            :rtype list[Hotel] or int: ->
            -> Список объектов типа Hotel в случае успешного ответа, или код ответа в случае неудачи.
        """

    check_in_date, check_out_date, rooms, region_id = data_list

    if filters is None:
        filters = {}

    if sort is None:
        sort = ""

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "rooms": rooms,
        "resultsStartingIndex": 0,
        "resultsSize": 30,
        "sort": sort,
        "filters": filters
    }

    response = func(url=url, payload=payload, headers=headers)

    return response


class SiteApiInterface:
    """Интерфейс для взаимодействия с сайтом API для получения списка отелей."""

    @staticmethod
    def get_hotels():
        """Возвращает функцию для получения списка отелей."""
        return _get_hotels


if __name__ == '__main__':
    SiteApiInterface()
