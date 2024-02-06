from datetime import date
from typing import Dict, List


def parse_date(date_data):
    return f"{date_data['year']}-{date_data['month']}-{date_data['day']}"


def format_user_data(user_input, rooms_db):
    user_data = [
        {'checkInDate': None},
        {'checkOutDate': None},
        {'rooms': None},
        {'city': None}
    ]

    check_in_date = format_date(user_input.check_in_date)
    check_out_date = format_date(user_input.check_out_date)
    rooms_list = format_rooms(rooms_db)

    user_data[0]["checkInDate"] = check_in_date
    user_data[1]["checkOutDate"] = check_out_date
    user_data[2]["rooms"] = rooms_list
    user_data[3]["city"] = user_input.city

    return user_data


def format_date(date_obj: date) -> Dict[str, int]:
    return {"year": date_obj.year, "month": date_obj.month, "day": date_obj.day}


def format_rooms(rooms_db) -> List[Dict[str, str]]:
    rooms_list = []
    for room in rooms_db:
        room_dict = {'adults': str(room.adults), 'children': str(room.children)}
        rooms_list.append(room_dict)
    return rooms_list