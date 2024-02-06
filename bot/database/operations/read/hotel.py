from bot.hotels_site_API import Hotel
from bot.database.models import HotelDB


def is_hotel_in_db(checking_hotel: Hotel):
    hotel_db = HotelDB.select().where(HotelDB.hotel_id == checking_hotel.id)
    return hotel_db


def get_user_hotels(user_tg_id):
    user_saved_hotels = HotelDB.select().where(HotelDB.user_telegram_id == user_tg_id)
    return user_saved_hotels
