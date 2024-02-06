from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.handlers.user.models import Room


def add_first_row_button(markup: InlineKeyboardMarkup, room_i):
    markup.row(InlineKeyboardButton(f"Комната {room_i}", callback_data="empty"))
    return markup


def add_adults_rows_buttons(markup: InlineKeyboardMarkup,
                            rooms_number: int, room_i: int, adults: int, children: int):
    markup.row(InlineKeyboardButton("Взрослых в комнате", callback_data="empty"))
    button_list = []
    for adults_button_i in range(1, 5):
        if adults_button_i == adults:
            button_list.append(InlineKeyboardButton(f"{adults_button_i} ☑",
                                            callback_data=f"rooms_count_{rooms_number}_room_{room_i}_"
                                                          f"adults_{adults_button_i}_children_{children}"))
        else:
            button_list.append(InlineKeyboardButton(f"{adults_button_i}",
                                            callback_data=f"rooms_count_{rooms_number}_room_{room_i}_"
                                                          f"adults_{adults_button_i}_children_{children}"))
    markup.row(*button_list)
    return markup


def add_children_rows_buttons(markup: InlineKeyboardMarkup,
                              rooms_number: int, room_i: int, adults: int, children: int):
    markup.row(InlineKeyboardButton("Детей в комнате", callback_data="empty"))
    button_list = []
    for children_button_i in range(4):
        if children_button_i == children:
            button_list.append(InlineKeyboardButton(f"{children_button_i} ☑",
                                            callback_data=f"rooms_count_{rooms_number}_room_{room_i}_"
                                                          f"adults_{adults}_children_{children_button_i}"))
        else:
            button_list.append(InlineKeyboardButton(f"{children_button_i}",
                                            callback_data=f"rooms_count_{rooms_number}_room_{room_i}_"
                                                          f"adults_{adults}_children_{children_button_i}"))
    markup.row(*button_list)
    return markup


def add_prev_next_room_buttons(markup: InlineKeyboardMarkup,
                               rooms_number: int, room_i: int):
    if room_i == rooms_number:
        finish_rooms_select_button = InlineKeyboardButton("Завершить выбор комнат",
                                                          callback_data="cont_")
        markup.row(finish_rooms_select_button)
        return markup
    elif room_i == 1:
        prev_room_button = InlineKeyboardButton("Комната 1", callback_data="empty")
        next_room_button = InlineKeyboardButton(f"Комната {room_i + 1}",
                                                callback_data=f"rooms_count_{rooms_number}_room_{room_i + 1}_"
                                                              f"adults_{1}_children_{0}")
        markup.row(prev_room_button, next_room_button)
    else:
        prev_room_button = InlineKeyboardButton(f"Комната {room_i - 1}",
                                                callback_data=f"rooms_count_{rooms_number}_room_{room_i - 1}_"
                                                              f"adults_{1}_children_{0}")
        next_room_button = InlineKeyboardButton(f"Комната {room_i + 1}",
                                                callback_data=f"rooms_count_{rooms_number}_room_{room_i + 1}_"
                                                              f"adults_{1}_children_{0}")
        markup.row(prev_room_button, next_room_button)

    return markup


def format_rooms(rooms: list):
    room_str = "\n"
    for i, room in enumerate(rooms, start=1):
        if room:
            adults = int(room.get('adults', 0))
            children = int(room.get('children', 0))
            room_str += f"Комната {i}: взрослых: {adults}, детей: {children}\n"
    return room_str


def convert_rooms_list_to_Rooms_list(rooms: list):
    rooms_list: list[Room] = []
    for room in rooms:
        rooms_list.append(Room(adults=int(room['adults']), children=int(room['children'])))

    return rooms_list
