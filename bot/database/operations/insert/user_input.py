from bot.database.models import UserInputDB


def insert_user_input(user_telegram_id, city, check_in_date, check_out_date):
    return UserInputDB.create(
        user_telegram_id=user_telegram_id,
        city=city,
        check_in_date=check_in_date,
        check_out_date=check_out_date
    )
