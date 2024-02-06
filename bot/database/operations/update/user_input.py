from peewee import DoesNotExist
from bot.database.models import UserInputDB


def update_user_input(user_telegram_id, city, check_in_date, check_out_date):
    try:
        user_input = UserInputDB.get(UserInputDB.user_telegram_id == user_telegram_id)
        # Обновление данных
        user_input.city = city
        user_input.check_in_date = check_in_date
        user_input.check_out_date = check_out_date
        user_input.save()
        print(f"Данные пользователя с user_telegram_id={user_telegram_id} успешно обновлены.")
    except DoesNotExist:
        print(f"Пользователь с user_telegram_id={user_telegram_id} не найден в таблице UserInput.")
