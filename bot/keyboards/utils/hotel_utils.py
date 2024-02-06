from bot.handlers.user.models import User
from bot.hotels_site_API.utils.comands.high_low_command import high_low_datas
from bot.hotels_site_API.utils.requests.API_datas_connection.site_api_connector import site, site_api
from bot.hotels_site_API.utils.requests.city_id_request.serchID import url, headers, site


def convert_user_input(user_input: list):
    converted_data = {}

    for item in user_input:
        if 'city' in item:
            city_value = item['city']
            if city_value.isdigit():
                return user_input

    for item in user_input:
        key, value = item.popitem()

        if key == 'rooms':
            converted_rooms = []
            for room in value:
                if not room:
                    print('skip')
                    continue
                adults = int(room.get('adults', 1))
                children_count = int(room.get('children', 0))

                if adults > 0 or children_count > 0:
                    children_list = [{'age': 12} for _ in range(children_count)]

                    room_dict = {
                        'adults': adults,
                        'children': children_list
                    }
                    converted_rooms.append(room_dict)

            converted_data[key] = converted_rooms

        else:
            converted_data[key] = value

        if key == 'city':
            get_city = site.get_city_id()
            city_id = get_city(url=url, headers=headers, city_name=value)
            converted_data[key] = city_id

    convert_to_list = []
    for item in converted_data:
        convert_to_list.append(converted_data[item])

    return convert_to_list


def convert_user_data_to_dicts_list(user: User):
    # to this ->
    # dicts_user_list = [
    #   {'checkInDate': {'year': 2024, 'month': 5, 'day': 14}},
    #   {'checkOutDate': {'year': 2024, 'month': 9, 'day': 20}},
    #   {'rooms': [{'adults': '2', 'children': '2'}, {'adults': '2', 'children': '1'}, {}]},
    #   {'city': 'Ottawa'}
    # ]


    user_date_city = user.input_data
    arrival_day = user_date_city.arrival_day
    arrival_month = user_date_city.arrival_month
    arrival_year = user_date_city.arrival_year

    departure_day = user_date_city.dep_day
    departure_month = user_date_city.dep_month
    departure_year = user_date_city.dep_year
    city = user_date_city.city

    rooms = user.get_rooms_list()

    dicts_user_list = [
      {'checkInDate': {'year': arrival_year, 'month': arrival_month, 'day': arrival_day}},
      {'checkOutDate': {'year': departure_year, 'month': departure_month, 'day': departure_day}},
      {'rooms': rooms},
      {'city': city}
    ]

    return dicts_user_list


def get_high_low_command_hotels(command_type, parameter_type, user: User):
    user_data_1 = convert_user_data_to_dicts_list(user)     # for second convert method
    user_data_2 = convert_user_input(user_data_1)           # for request to API

    is_high = False
    if command_type == 'high':
        is_high = True

    if parameter_type == 'price':
        hotels = high_low_datas(data_list=user_data_2, high_sort=is_high, is_price=True)
    elif parameter_type == 'score':
        hotels = high_low_datas(data_list=user_data_2, high_sort=is_high, is_scores=True)
    elif parameter_type == 'distance':
        hotels = high_low_datas(data_list=user_data_2, high_sort=is_high, is_distance=True)
    else:
        hotels = high_low_datas(data_list=user_data_2, high_sort=is_high)

    return hotels


def correct_filter_data(filter_data: dict):
    stars_list = []
    min_star = filter_data["star"]
    if min_star == 2:
        stars_list = ["20", "30", "40", "50"]
    elif min_star == 3:
        stars_list = ["30", "40", "50"]
    elif min_star == 4:
        stars_list = ["40", "50"]
    elif min_star == 5:
        stars_list = ["50"]

    filter_data["star"] = stars_list

    if filter_data["guestRating"] == "8":
        filter_data["guestRating"] = "35"

    elif filter_data["guestRating"] == "9":
        filter_data["guestRating"] = "40"

    else:
        filter_data.pop("guestRating")

    return filter_data


def get_custom_command_hotels(user: User, filter_data: dict, count_hotels=7):
    user_data_1 = convert_user_data_to_dicts_list(user)  # for second convert method
    user_data_2 = convert_user_input(user_data_1)  # for request to API

    filter_data = correct_filter_data(filter_data)

    get_hotels = site_api.get_hotels()
    all_city_hotels = get_hotels(url=url, headers=headers, data_list=user_data_2,
                                 filters=filter_data)

    return all_city_hotels[:count_hotels]

    # all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
    #                              filters={"star": [stars_hotel_count]})
    #
    # all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
    #                              filters={"amenities": ["POOL"]})

