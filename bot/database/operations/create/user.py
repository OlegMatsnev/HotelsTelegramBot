from bot.database.models import UserDB


def create_user(user_telegram_id, username):
    UserDB.get_or_create(
        telegram_id=user_telegram_id,
        username=username
    )
