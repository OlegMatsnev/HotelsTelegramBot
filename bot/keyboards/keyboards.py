from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .utils.calendar_utils import second_row, first_row, call_arrival_month_calendar, prev_next_month_button, Calendar, \
    get_next_last_data, call_departure_start_month_calendar, \
    call_departure_last_month_calendar, get_date_caption
from .utils.room_menu_utils import add_first_row_button, add_adults_rows_buttons, \
    add_children_rows_buttons, add_prev_next_room_buttons, format_rooms, convert_rooms_list_to_Rooms_list
from ..handlers.user.models import User, UserInput
from bot.database import get_saved_input
from ..hotels_site_API.utils.hotel import Hotel


def calendar_keyboard(year_num: (int, None), month_num: (int, None)) -> InlineKeyboardMarkup:
    if not year_num or not month_num:
        year_num = Calendar.current_year
        month_num = Calendar.current_month

    # first row: month name + year (январь 2024)
    # second row: weekdays (Пн Вт Ср Чт Пт Сб Вс)
    # other rows: all month days

    markup = InlineKeyboardMarkup()

    markup = first_row(year=year_num, month_num=month_num, markup=markup)
    markup = second_row(markup=markup)
    markup = call_arrival_month_calendar(year=year_num, month=month_num, markup=markup)
    markup = prev_next_month_button(year=year_num, month=month_num, markup=markup)

    return markup


def departure_calendar_keyboard(year: int, month: int, day: int):
    # there I will output 1-2 months in one markup, because it's enough for 28 days.
    # 28 due to limit of hotels.com website search
    # so, there will be 1 and max 2 months

    markup = InlineKeyboardMarkup()

    # getting start date data (tomorrow after arrival date)
    # also getting date in 28 dats after arrival date
    start_day, start_month, start_year = get_next_last_data(year, month, day, next_day=1)
    last_day, last_month, last_year = get_next_last_data(year, month, day, next_day=28)

    markup = first_row(year=start_year, month_num=start_month, markup=markup)
    markup = second_row(markup=markup)

    # if we have 1 month
    if start_month == last_month:
        markup = call_departure_start_month_calendar(start_year=start_year, start_month=start_month,
                                                     start_day=start_day - 1,
                                                     markup=markup, first_month_days=last_day)
    # 2 months in this case
    else:
        markup = call_departure_start_month_calendar(start_year=start_year, start_month=start_month,
                                                     start_day=start_day - 1,
                                                     markup=markup)
        # for second month
        markup = first_row(last_year, last_month, markup)
        markup = second_row(markup=markup)
        markup = call_departure_last_month_calendar(last_day=last_day, last_month=last_month, last_year=last_year,
                                                    markup=markup)

    return markup


def rooms_start_menu():
    # show keyboard with the choice of number rooms

    markup = InlineKeyboardMarkup()

    rooms_num_1_button = InlineKeyboardButton(str(1), callback_data='rooms_count_1_room_1_adults_1_children_0')
    rooms_num_2_button = InlineKeyboardButton(str(2), callback_data='rooms_count_2_room_1_adults_1_children_0')
    rooms_num_3_button = InlineKeyboardButton(str(3), callback_data='rooms_count_3_room_1_adults_1_children_0')
    rooms_num_4_button = InlineKeyboardButton(str(4), callback_data='rooms_count_4_room_1_adults_1_children_0')

    markup.row(rooms_num_1_button, rooms_num_2_button, rooms_num_3_button, rooms_num_4_button)

    # back_button = InlineKeyboardButton("Назад", callback_data='departure_month_')
    # markup.row(back_button)

    return markup


def room_keyboard(rooms_number, room_i, adults, children):
    # first row - num of room, for instance: Комната 1
    # second row - Взрослых в комнате
    # third row - [1] 2 3 4, [] -> selected room, default value 1
    # 4-th row - Детей в комнате:
    # 5-th row - [0] 1 2 3, [] -> selected room, default value 1
    # 6-th row - prev room button and next room button

    markup = InlineKeyboardMarkup()
    markup = add_first_row_button(markup=markup, room_i=room_i)
    markup = add_adults_rows_buttons(markup, rooms_number, room_i, adults, children)
    markup = add_children_rows_buttons(markup, rooms_number, room_i, adults, children)
    markup = add_prev_next_room_buttons(markup, rooms_number, room_i)

    return markup


def countries_info():
    markup = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton("Назад", callback_data='cont_')
    markup.row(back_button)

    info_str = 'Здесь представлены все страны и их города, которые доступны на данный момент:\n' \
               '🇺🇸 - США (Нью Йорк, Майми, Лос Анджелес, Лас Вегас)\n' \
               '🇨🇦 - Канада\n' \
               '🇲🇽 - Мексика'

    return markup, info_str


def save_input_to_db_menu(user: User):
    # caption
    user_input: UserInput = user.input_data
    user_input_dict = user_input.to_dict()

    date_str = get_date_caption(user_input_date=user_input_dict)    # date info
    rooms_info = user.get_rooms_list()                              # rooms list
    formatted_rooms = format_rooms(rooms_info)                      # rooms info
    city_name = user_input_dict.get('city', None)                   # city name

    caption = f"Сохранить введенные данные для следующих запросов?\n\n" \
              f"{date_str}\n" \
              f"{formatted_rooms}\n" \
              f"Город: {city_name}"
    # markup
    markup = InlineKeyboardMarkup()
    item2 = InlineKeyboardButton("Не сохранять", callback_data='input_save_0')
    item1 = InlineKeyboardButton("Сохранить", callback_data='input_save_1')
    markup.row(item1, item2)

    return caption, markup


def select_search_command():
    markup = InlineKeyboardMarkup()

    low_button = InlineKeyboardButton("low", callback_data="command_low")
    high_button = InlineKeyboardButton("high", callback_data="command_high")
    custom_button = InlineKeyboardButton("custom", callback_data="custom")
    back_button = InlineKeyboardButton("Главное меню", callback_data='back')

    markup.row(low_button, high_button, custom_button)
    markup.row(back_button)

    return markup


def using_saved_input(user: User) -> (str, InlineKeyboardMarkup):
    # will return db data in User object format; markup and caption for bot.edit

    # getting this ->
    # user_data = [
    #     {'checkInDate': None},
    #     {'checkOutDate': None},
    #     {'rooms': None},
    #     {'city': None}
    # ]
    user_data = get_saved_input(user.telegram_id)

    # getting data
    arrive_day = user_data[0]["checkInDate"]["day"]
    arrive_month = user_data[0]["checkInDate"]["month"]
    arrive_year = user_data[0]["checkInDate"]["year"]
    departure_day = user_data[1]["checkOutDate"]["day"]
    departure_month = user_data[1]["checkOutDate"]["month"]
    departure_year = user_data[1]["checkOutDate"]["year"]
    city = user_data[3].get('city', None)
    rooms = user_data[2].get('rooms')

    # creating User class object
    user_input = UserInput(arrive_year, arrive_month, arrive_day, departure_year, departure_month, departure_day, city)
    user_input_dict = user_input.to_dict()
    user.rooms = convert_rooms_list_to_Rooms_list(rooms=rooms)
    user.input_data = user_input

    # creating caption for bot.edit
    date_str = get_date_caption(user_input_date=user_input_dict)            # date info
    rooms_info = user.get_rooms_list()                                      # rooms list
    formatted_rooms = format_rooms(rooms_info)                              # rooms info
    city_name = user_input_dict.get('city', None)                           # city name

    caption = f"Использовать введенные раннее данные?\n\n" \
              f"{date_str}\n" \
              f"{formatted_rooms}\n" \
              f"Город: {city_name}"

    # creating markup keyboard
    markup = InlineKeyboardMarkup()
    item2 = InlineKeyboardButton("Нет", callback_data='search_hotels')
    item1 = InlineKeyboardButton("Да", callback_data='input_save_0')
    markup.row(item1, item2)

    return caption, markup


def chose_search_hotels_parameter(command_type):
    markup = InlineKeyboardMarkup()

    price_button = InlineKeyboardButton("Цена", callback_data=f"command_{command_type}_parameter_price")
    score_button = InlineKeyboardButton("Оценка", callback_data=f"command_{command_type}_parameter_score")
    distance_button = InlineKeyboardButton("Центр", callback_data=f"command_{command_type}_parameter_distance")

    back_button = InlineKeyboardButton("Назад", callback_data="input_save_0")
    markup.row(price_button, score_button, distance_button)
    markup.row(back_button)

    return markup


def get_hotel_keyboard(callback_str: str, hotels_num: int):
    # callback_str example: hotel_1 or hotel_1_save
    markup = InlineKeyboardMarkup()

    if callback_str.endswith("_save"):
        save_hotel_button_text = "Сохранено ✅"
    else:
        save_hotel_button_text = "Сохранить"

    ordering_hotels_num = int(callback_str.split("_")[1])
    callback_str = "hotel_"

    if ordering_hotels_num == 1:
        callback_left_str = "empty"
        callback_right_str = callback_str + str(ordering_hotels_num + 1)

    elif ordering_hotels_num == 5 or ordering_hotels_num == hotels_num:
        callback_left_str = callback_str + str(ordering_hotels_num - 1)
        callback_right_str = "empty"

    else:
        callback_left_str = callback_str + str(ordering_hotels_num - 1)
        callback_right_str = callback_str + str(ordering_hotels_num + 1)

    move_left_button = InlineKeyboardButton("◀", callback_data=callback_left_str)
    move_right_button = InlineKeyboardButton("▶", callback_data=callback_right_str)
    save_hotel_button = InlineKeyboardButton(save_hotel_button_text,
                                             callback_data=callback_str + str(ordering_hotels_num) + "_save")

    markup.row(move_left_button, save_hotel_button, move_right_button)
    return markup






