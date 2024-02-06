from bot.database.models import RoomDB


def insert_room(adults, children, user_telegram_id):
    return RoomDB.create(
        adults=adults,
        children=children,
        user_telegram_id=user_telegram_id
    )
