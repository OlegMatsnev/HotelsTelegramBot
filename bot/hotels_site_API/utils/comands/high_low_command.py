from bot.hotels_site_API.utils.requests.API_datas_connection.site_api_connector import url, headers, site_api
from bot.hotels_site_API.utils.hotel import Hotel

# Получение ссылки на функцию, для получения списка отелей
# с использованием функции get_city_id() из другого модуля
get_hotels = site_api.get_hotels()


def del_unpopular_hotels(hotels: list[Hotel]):
    """
        Функция фильтрует отели, оставляя только те, у которых больше 10 отзывов.

        Args:
            hotels (list[Hotel]): Список объектов типа Hotel.

        Returns:
            :return new_list (filtered list)
            :rtype list[Hotel]: Отфильтрованный список отелей с более чем 10 отзывами.
        """

    new_list: list[Hotel] = []

    for hotel in hotels:
        if hotel.reviews_count >= 10:
            new_list.append(hotel)

    return new_list


def high_low_datas(data_list: list, high_sort=False, count_hotels=5,
                   is_price=False, is_scores=False, is_distance=False) -> (list[Hotel], None):

    """
    Функция сортирует отели по различным критериям.

    Args:
        data_list (list): Список данных о поиске (дата приезда, дата отъезда, комнаты и город).
        high_sort (bool): Сортировать по убыванию (если True) или по возрастанию (если False).
        count_hotels (int): Количество отелей для выбора (по умолчанию = 5).
        is_price (bool): Сортировать по цене.
        is_scores (bool): Сортировать по рейтингу отелей.
        is_distance (bool): Сортировать по расстоянию до центра.

    Returns:
        :return sorted list
        :rtype list[Hotel]: list[Hotel] or None: ->
        -> Отсортированный список отелей или None, если не указан ни один критерий сортировки.
    """

    if is_price:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list, sort="PRICE_LOW_TO_HIGH")
        if high_sort:
            return all_city_hotels[-count_hotels:]
        else:
            return all_city_hotels[:count_hotels]

    if is_scores:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list, sort="REVIEW")
        only_popular_reviews_list = del_unpopular_hotels(all_city_hotels)
        scores_sorted_hotels_list = sorted(only_popular_reviews_list, key=lambda hotel: hotel.reviews_score,
                                           reverse=high_sort)
        result_list = scores_sorted_hotels_list[:count_hotels]
        return result_list

    if is_distance:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list, sort="DISTANCE")
        if high_sort:
            return all_city_hotels[:count_hotels]
        else:
            return all_city_hotels[-count_hotels:]
