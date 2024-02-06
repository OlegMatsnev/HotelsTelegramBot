import json

from telebot import types
from telebot.types import WebAppInfo

from bot.keyboards import calendar_keyboard, departure_calendar_keyboard, \
    rooms_start_menu, room_keyboard, \
    countries_info, save_input_to_db_menu, select_search_command, using_saved_input, chose_search_hotels_parameter, \
    get_hotel_keyboard
from .models import User, UserInput, Room
from ...keyboards.utils.cities_menu import get_country
from ...keyboards.utils.hotel_utils import get_high_low_command_hotels, get_custom_command_hotels
from bot.database import save_input_to_db, save_hotel_to_db
from bot.database.operations import get_db_user_input


# TODO: add comments, documentation and logging


def register_user_handlers(bot):
    user = User()

    @bot.message_handler(commands=['start'])
    def start_ex(message):
        user.telegram_id = message.chat.id
        user.name = message.chat.username

        callback_str = 'search_hotels'
        if get_db_user_input(user.telegram_id):
            callback_str = 'db_input'

        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Инструкция", callback_data='instruction')
        item2 = types.InlineKeyboardButton("Сайт", callback_data='website')
        item3 = types.InlineKeyboardButton("Поиск отелей", callback_data=callback_str)
        item4 = types.InlineKeyboardButton("Сохранённые отели", callback_data='saved_hotels')

        markup.row(item1, item2)
        markup.row(item3)
        markup.row(item4)

        bot.send_photo(message.chat.id, 'https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg',
                       caption=f'Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}! 👋',
                       reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'db_input')
    def use_save_data_menu(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        caption, markup = using_saved_input(user)
        print(user.rooms)

        bot.edit_message_caption(caption=caption, chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    """Arrival data"""

    user_input = UserInput()

    @bot.callback_query_handler(func=lambda call: call.data == 'search_hotels' or call.data.startswith("arrival_data"))
    def get_arrival_data(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        callback_str: str = callback.data
        if callback_str == 'search_hotels':
            markup = calendar_keyboard(year_num=None, month_num=None)
        else:
            year = int(callback_str.split("_")[2])
            month = int(callback_str.split("_")[3])
            markup = calendar_keyboard(year_num=year, month_num=month)

        bot.edit_message_caption(caption='Выберите день прибытия:', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    """Departure data"""

    # getting arrival data and show departure calendar menu
    @bot.callback_query_handler(func=lambda call: call.data.startswith("arrival_year_"))
    def get_departure_data(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        nonlocal user_input
        callback_str: str = callback.data
        if callback_str.startswith("arrival_year_"):
            arrival_year: int = int(callback_str.split("_")[2])
            arrival_month: int = int(callback_str.split("_")[4])
            arrival_day: int = int(callback_str.split("_")[6])

            user_input.arrival_year = arrival_year
            user_input.arrival_month = arrival_month
            user_input.arrival_day = arrival_day

            markup = departure_calendar_keyboard(arrival_year, arrival_month, arrival_day)
        else:
            markup = departure_calendar_keyboard(user_input.arrival_year, user_input.arrival_month,
                                                 user_input.arrival_day)
        print(user_input.arrival_day)
        bot.edit_message_caption(caption='Выберите день отбытия:', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("departure") or
                                                  call.data.startswith("rooms_count_"))
    def get_arrival_data(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id
        callback_str: str = callback.data

        if callback_str.startswith("departure"):
            # parsing departure date
            # example: departure_year_2024_month_3_day_28
            departure_year: int = int(callback_str.split("_")[2])
            departure_month: int = int(callback_str.split("_")[4])
            departure_day: int = int(callback_str.split("_")[6])

            user_input.dep_year = departure_year
            user_input.dep_month = departure_month
            user_input.dep_day = departure_day

            # show room menu
            markup = rooms_start_menu()
            caption = "Выберите количество комнат для заселения (от 1 до 4):"

            if len(user.rooms) > 0:
                user.rooms = []

        else:
            # example: rooms_count_3_room_1_adults_1_children_0
            # getting rooms number, room number, adults count, children count
            rooms_count = int(callback_str.split("_")[2])
            room_i = int(callback_str.split("_")[4])
            adults = int(callback_str.split("_")[6])
            children = int(callback_str.split("_")[8])

            # filling rooms list to use update method
            if len(user.rooms) == 0:
                for user_room_i in range(rooms_count):
                    user.add_room(Room(1, 0))  # -> default room

            user.update_room(room_i - 1, Room(adults, children))

            markup = room_keyboard(rooms_number=rooms_count, room_i=room_i, adults=adults, children=children)
            caption = f"Выберите соответствующие данные для комнаты №{room_i}:"

        # for i in user.rooms:
        #     print(i)

        try:
            bot.edit_message_caption(caption=caption, chat_id=chat_id,
                                     reply_markup=markup, message_id=message_id)
        except Exception as e:
            if "message is not modified" in str(e):
                # Проигнорировать ошибку, так как сообщение не изменилось
                pass
            else:
                # Обработать другие исключения, если это не "message is not modified"
                print(f"Произошла ошибка: {e}")

    """City"""

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cont_'))
    def chose_country(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        if callback.data == 'cont_':
            callback.data = "cont_Europe_country_Italy"  # start value

        markup = get_country(callback=callback)

        try:
            bot.edit_message_caption(caption='Время выбрать город - начнём с континента!', chat_id=chat_id,
                                     reply_markup=markup, message_id=message_id)
        except Exception as e:
            if "message is not modified" in str(e):
                # Проигнорировать ошибку, так как сообщение не изменилось
                pass
            else:
                # Обработать другие исключения, если это не "message is not modified"
                print(f"Произошла ошибка: {e}")

    @bot.callback_query_handler(func=lambda call: call.data == 'countries_info')
    def counties_info_menu(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        markup, info_str = countries_info()

        bot.edit_message_caption(caption=info_str, chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    """Save input data menu"""

    @bot.callback_query_handler(func=lambda call: call.data.startswith('city_'))
    def save_input(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        # callback example: city_Los Angeles
        user_input.city = callback.data.split('_')[1]
        user.input_data = user_input

        caption, markup = save_input_to_db_menu(user)

        bot.edit_message_caption(caption=caption, chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    """Commands: low, high, custom"""

    @bot.callback_query_handler(func=lambda call: call.data == 'input_save_0' or call.data == 'input_save_1' or
                                call.data == "from_hotels_menu_back_to_commands_menu")
    def select_command(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        # convert user data for db methods
        user_data = user.convert_to_dicts_list()
        if callback.data == "input_save_1":
            # saving in user data in database
            save_input_to_db(user_data, user.telegram_id, user.name)
        markup = select_search_command()

        # if we back from hotels list -> we need to update our photo
        if callback.data == 'from_hotels_menu_back_to_commands_menu':
            bot.edit_message_media(
                media=types.InputMediaPhoto('https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg'),
                chat_id=chat_id, message_id=message_id)

        bot.edit_message_caption(caption='Команды для поиска:', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    """Categories of high/low commands"""

    @bot.callback_query_handler(func=lambda call: call.data == 'command_low' or call.data == 'command_high')
    def select_category(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        callback_str = callback.data
        command_type = callback_str.split("_")[1]
        markup = chose_search_hotels_parameter(command_type)

        bot.edit_message_caption(caption=f'Категории команды {command_type}:', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('command_low_parameter_') or
                                                  call.data.startswith('command_high_parameter_'))
    def show_first_hotel(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        # firstly we need to get hotels to show them.
        # define parameter for searching:
        callback_str = callback.data
        command_type = callback_str.split("_")[1]
        parameter_type = callback_str.split("_")[3]
        user.hotels = get_high_low_command_hotels(command_type=command_type, parameter_type=parameter_type, user=user)
        hotels_num = len(user.hotels)
        markup = get_hotel_keyboard("hotel_1", hotels_num)

        hotel = user.hotels[0]

        bot.edit_message_media(media=types.InputMediaPhoto(f'{hotel.picture_url}'),
                               chat_id=chat_id, message_id=message_id)

        try:
            bot.edit_message_caption(caption="Данные об отеле:\n"
                                             "{hotel_data} ".format(hotel_data=hotel),
                                     message_id=message_id,
                                     chat_id=chat_id,
                                     reply_markup=markup)
        except Exception as e:
            if "message is not modified" in str(e):
                # Проигнорировать ошибку, так как сообщение не изменилось
                pass
            else:
                # Обработать другие исключения, если это не "message is not modified"
                print(f"Произошла ошибка: {e}")

        # so, now we can show our hotels in telegram:

    """Custom command"""

    delete_message = None

    @bot.callback_query_handler(func=lambda call: call.data == "custom")
    def custom_message(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        bot.delete_message(chat_id=chat_id, message_id=message_id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Открыть веб страницу',
                                        web_app=WebAppInfo(url='https://olegmatsnev.github.io/TeleBot/index.html')))

        global delete_message
        delete_message = bot.send_photo(chat_id, 'https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg',
                                        caption="Нажмите кнопку под клавиатурой",
                                        reply_markup=markup)

    @bot.message_handler(content_types=["web_app_data"])  # получаем отправленные данные
    def answer(webAppMes):

        print(delete_message)
        print(webAppMes)  # вся информация о сообщении
        print(webAppMes.web_app_data.data)  # конкретно то что мы передали в бота
        bot.delete_message(webAppMes.chat.id, delete_message.id)

        # Преобразовать строку JSON в словарь
        data_dict = json.loads(webAppMes.web_app_data.data)

        user.hotels = get_custom_command_hotels(user=user, filter_data=data_dict)
        hotels_num = len(user.hotels)
        markup = get_hotel_keyboard("hotel_1", hotels_num)

        hotel = user.hotels[0]

        bot.send_photo(webAppMes.chat.id, f'{hotel.picture_url}',
                       caption="Данные об отеле:\n"
                               "{hotel_data} ".format(hotel_data=hotel), reply_markup=markup)

    """Output hotels info"""

    @bot.callback_query_handler(func=lambda call: call.data.startswith('hotel_'))
    def show_hotels(callback):
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id

        callback_str: str = callback.data

        hotel_i = int(callback_str.split("_")[1]) - 1
        hotels_num = len(user.hotels)
        hotel = user.hotels[hotel_i]

        if callback_str.endswith("_save"):
            save_hotel_to_db(hotel=hotel, user_telegram_id=user.telegram_id, user_name=user.name)

        markup = get_hotel_keyboard(callback_str, hotels_num)

        bot.edit_message_media(media=types.InputMediaPhoto(f'{hotel.picture_url}'),
                               chat_id=chat_id, message_id=message_id)

        try:
            bot.edit_message_caption(caption="Данные об отеле:\n"
                                             "{hotel_data} ".format(hotel_data=hotel),
                                     message_id=message_id,
                                     chat_id=chat_id,
                                     reply_markup=markup)
        except Exception as e:
            if "message is not modified" in str(e):
                # Проигнорировать ошибку, так как сообщение не изменилось
                pass
            else:
                # Обработать другие исключения, если это не "message is not modified"
                print(f"Произошла ошибка: {e}")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == 'instruction':
            pass

            markup = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton("Назад", callback_data='back')
            markup.row(back_button)
            bot.edit_message_media(
                media=types.InputMediaPhoto('https://bnovo.ru/wp-content/uploads/2021/11/registration'
                                            '-of-guests-at-the-hotel-4-800.jpg'),
                chat_id=chat_id, message_id=message_id)
            bot.edit_message_caption(caption='Это инструкция, здесь должен быть ваш текст инструкции.', chat_id=chat_id,
                                     reply_markup=markup, message_id=message_id)
            # bot.answer_callback_query(callback_query_id=call.id, text="THIS IS AN ALERT", show_alert=True)
        elif call.data == 'website':
            pass
            # custom_message(callback=call)
            # bot.delete_message(chat_id=chat_id, message_id=message_id)
            #
            # markup = types.ReplyKeyboardMarkup()
            # markup.add(types.KeyboardButton('Открыть веб страницу',
            #                                 web_app=WebAppInfo(url='https://olegmatsnev.github.io/TeleBot/index.html')),
            #            types.KeyboardButton('Пусто'))
            # global message_global
            # message_global = bot.send_photo(chat_id, 'https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg',
            #                caption="Нажмите кнопку под клавиатурой",
            #                reply_markup=markup)

        elif call.data == 'back':
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Инструкция", callback_data='instruction')
            item2 = types.InlineKeyboardButton("Сайт", callback_data='website')
            markup.row(item1, item2)
            item3 = types.InlineKeyboardButton("Поиск отелей", callback_data='search_hotels')
            markup.row(item3)
            bot.edit_message_media(
                media=types.InputMediaPhoto('https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg'),
                chat_id=chat_id, message_id=message_id)
            bot.edit_message_caption(caption='Главное меню.', chat_id=chat_id,
                                     reply_markup=markup, message_id=message_id)
            # chat_id_text = bot.send_message(call.from_user.id, text="s", reply_markup=ReplyKeyboardRemove())

# Другие обработчики для пользователей
# ...
