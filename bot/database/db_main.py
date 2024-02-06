from datetime import date
from typing import List, Dict
from bot.database.db_main_utils import *

from bot.database.models import HotelDB
from bot.hotels_site_API import Hotel


from .operations import \
    update_user_input, \
    delete_rooms_for_user_input, \
    insert_user_input, insert_room, \
    get_db_user_input, create_user, \
    read_db_user, get_user_rooms, \
    is_hotel_in_db, insert_hotel, \
    get_user_hotels


def save_input_to_db(user_data, user_telegram_id, user_name):

    create_user(user_telegram_id, user_name)
    # example user_data
    # [{'checkInDate': {'day': 15, 'month': 2, 'year': 2024}, 'checkOutDate': {'day': 10, 'month': 3, 'year': 2024},
    #   'city': 'Rome'}, [{'adults': '3', 'children': '1'}, {'adults': '2', 'children': '0'}]]

    check_in_date_str = parse_date(user_data[0]['checkInDate'])
    check_out_date_str = parse_date(user_data[0]['checkOutDate'])
    city = user_data[0]['city']
    rooms_data = user_data[1]

    user_input = get_db_user_input(user_telegram_id)

    if user_input:
        update_user_input(user_telegram_id, city, check_in_date_str, check_out_date_str)
        delete_rooms_for_user_input(user_telegram_id)
    else:
        insert_user_input(user_telegram_id, city, check_in_date_str, check_out_date_str)

    for room_data in rooms_data:
        if room_data:
            adults = int(room_data.get('adults'))
            children = int(room_data.get('children'))
            insert_room(adults, children, user_telegram_id)


def get_saved_input(user_id):
    # user_data ->
    # [
    #   {'checkInDate': {'year': 2024, 'month': 5, 'day': 14}},
    #   {'checkOutDate': {'year': 2024, 'month': 9, 'day': 20}},
    #   {'rooms': [{'adults': '2', 'children': '2'}, {'adults': '2', 'children': '1'}, {}]},
    #   {'city': 'Ottawa'}
    # ]

    # Get the user with the given user_id
    user = read_db_user(user_id)

    if user:
        user_input = get_db_user_input(user_id)
        rooms_db = get_user_rooms(user_id)
        return format_user_data(user_input, rooms_db)
    else:
        return None


def save_hotel_to_db(hotel: Hotel, user_telegram_id, user_name):
    create_user(user_telegram_id, user_name)

    if is_hotel_in_db(hotel):
        return

    insert_hotel(hotel, user_telegram_id)


def get_saved_hotels(user_id):
    saved_hotels = get_user_hotels(user_id)

    if saved_hotels:
        hotels_list: list[HotelDB] = []

        for db_hotel in saved_hotels:
            hotels_list.append(
                HotelDB(
                    name=db_hotel.name,
                    picture_url=db_hotel.picture_url,
                    price_per_night=db_hotel.price_per_night,
                    total_price=db_hotel.total_price,
                    reviews_count=db_hotel.reviews_count,
                    reviews_score=db_hotel.reviews_score,
                    destination_info=db_hotel.destination_info,
                    hotel_id=db_hotel.hotel_id
                )
            )
        return hotels_list

    return None


def test_save_user_input():
    user_data = [{'checkInDate': {'year': 2024, 'month': 8, 'day': 1}},
                 {'checkOutDate': {'year': 2024, 'month': 12, 'day': 7}},
                 {'rooms': [{'adults': '1', 'children': '1'}, {'adults': '2', 'children': '0'}, {}]},
                 {'city': 'Miami'}]
    save_input_to_db(user_data, 22, "Oleg")


def test_get_user_input():
    print(get_saved_input(22))


def test_saving_hotel_to_db():
    hotel_test = Hotel(
        name="Отель C",
        is_available=True,
        min_rooms_left=3,
        picture_url="https://example.com/hotel.jpg",
        price_per_night=222.0,
        total_price=2010.0,
        reviews_count=520,
        reviews_score=3.5,
        destination_info="5 миль от центра",
        id=223
    )

    save_hotel_to_db(hotel_test, 177, "Dima")


def test_getting_saved_user_hotels():
    print(get_saved_hotels(177))


# test_saving_hotel_to_db()
# test_getting_saved_user_hotels()
