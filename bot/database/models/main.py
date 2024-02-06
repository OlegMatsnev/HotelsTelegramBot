# database/models/__init__.py
from .user_db import UserDB
from .user_input_db import UserInputDB
from .room_db import RoomDB
from .hotel_db import HotelDB


# TODO: add constraints for all requiring classes fields in models

def get_all_models():
    return [UserDB, UserInputDB, RoomDB, HotelDB]

