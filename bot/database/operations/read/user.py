from bot.database.models import UserDB


def read_db_user(telegram_id):
    user = UserDB.get_or_none(UserDB.telegram_id == telegram_id)
    return user
