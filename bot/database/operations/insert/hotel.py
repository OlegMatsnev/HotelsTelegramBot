from bot.database.models import HotelDB


def insert_hotel(hotel, user_telegram_id):

    # Extract hotel information
    name = hotel.name
    picture_url = hotel.picture_url
    price_per_night = hotel.price_per_night
    total_price = hotel.total_price
    reviews_count = hotel.reviews_count
    reviews_score = hotel.reviews_score
    destination_info = hotel.destination_info
    id = hotel.id

    # Create a new hotel record in the database
    HotelDB.create(
        hotel_id=id,
        name=name,
        picture_url=picture_url,
        price_per_night=price_per_night,
        total_price=total_price,
        reviews_count=reviews_count,
        reviews_score=reviews_score,
        destination_info=destination_info,
        user_telegram_id=user_telegram_id
    )
