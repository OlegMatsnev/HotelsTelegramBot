# bot/database/operations/delete.py
from bot.database.models import RoomDB


def delete_rooms_for_user_input(tg_id):
    RoomDB.delete().where(RoomDB.user_telegram_id == tg_id).execute()
