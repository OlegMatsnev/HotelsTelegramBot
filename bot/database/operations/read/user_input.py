from peewee import DoesNotExist
from bot.database.models import UserInputDB


def get_db_user_input(user_telegram_id):
    try:
        user_input = UserInputDB.get(UserInputDB.user_telegram_id == user_telegram_id)
        return user_input
    except DoesNotExist:
        print(f"UserInput not found for user_telegram_id: {user_telegram_id}")
        return None
