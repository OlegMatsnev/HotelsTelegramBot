from peewee import DoesNotExist
from bot.database.models import RoomDB


def get_user_rooms(user_telegram_id):
    try:
        rooms = RoomDB.select().where((RoomDB.user_telegram_id == user_telegram_id))
        return rooms
    except DoesNotExist:
        print(f"UserInput not found for user_telegram_id: {user_telegram_id}")
        return None
