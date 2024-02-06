import datetime
from typing import Dict
from bot.hotels_site_API.utils.requests.city_id_request.serchID import url, headers, site

# Получение ссылки на функцию, для получения ID города с использованием функции get_city_id() из другого модуля
get_city = site.get_city_id()


def validate_date(day: str, month: str, year: str) -> ((int, int, int), None):
    """
        Проверяет и делает валидацию введенной пользователем дату.

        Args:
            day (str), month (str), year (str): День, Месяц, Год в виде строки.

        Returns:
            :return data of data
            :rtype Tuple[int, int, int] or None: Кортеж с целыми числами (день, месяц, год)
                                                        или None в случае некорректного ввода.
    """

    try:
        day = int(day)
        month = int(month)
        year = int(year)

        start_year = datetime.datetime.now().year

        if not ((1 <= day <= 31) & (1 <= month <= 12) & (start_year <= year <= start_year + 1)):
            return False

        return day, month, year

    except ValueError:
        return False


def get_user_date_input(message: str) -> Dict:

    """
    Запрашивает и делает валидацию ввод(а) пользователя для даты (день, месяц, год).

    Args:
        message (str): Сообщение для пользователя.

    Returns:
        :return dictionary of data
        :rtype Dict (Словарь с данными о дате (день, месяц, год).)
    """

    while True:

        try:
            day, month, year = input(message).split()
            day, month, year = validate_date(day.lstrip("0"), month.lstrip("0"), year)
        except (TypeError, ValueError):
            print("Некорректная дата. Пожалуйста, введите дату в формате 'день месяц год' (например, 5 9 2023).")
            continue

        date = {"day": day, "month": month, "year": year}
        return date


def get_datas() -> (str, str):
    """
        Получает данные о дате приезда и отъезда.
        Делает валидацию данных о дате приезда и отъезда.

        Returns:
            :return tuple of datas about arrival and departure
            :rtype Tuple[str, str]: Кортеж с данными о датах приезда и отъезда (в виде строк).
        """

    while True:
        print('Пример ввода даты: 5 9 2023 (5 сентября 2023) ')
        check_in_date = get_user_date_input("Введите дату приезда в отель (день месяц год): ")
        check_out_date = get_user_date_input("Введите дату отъезда из отеля (день месяц год): ")

        if check_out_date["year"] < check_in_date["year"] or \
                (check_out_date["year"] == check_in_date["year"] and check_out_date["month"] < check_in_date[
                    "month"]) or \
                (check_out_date["year"] == check_in_date["year"] and check_out_date["month"] == check_in_date[
                    "month"] and
                 check_out_date["day"] < check_in_date["day"]):
            print("Дата отъезда не может быть раньше даты приезда. Пожалуйста, введите корректные даты.")
        else:
            break

    return check_in_date, check_out_date


def get_info() -> None:

    """Выводит информацию для пользователя о необходимых параметрах выбора отеля."""

    print("Для выбора отеля вам нужно указать такие параметры как:")
    print("\t1) Дата приезда и отъезда из отеля;")
    print("\t2) Количество комнат и количество детей и взрослых в каждой из комнат")
    print("\t3) Город, в каком находится отель.\n")


def get_rooms() -> list:
    """
        Запрашивает данные о количестве комнат и количестве взрослых и детей в каждой комнате.
        Делает валидацию данных.
        Returns:
            :return list of rooms with an adults and kids.
            :rtype list: Список с данными о комнатах (количество взрослых и детей).
    """

    while True:

        try:
            room_count = int(input("\nВведите количество комнат: "))
            if room_count < 1 or room_count > 4:
                print("Количество комнат должно быть от 1 до 4.")
            else:
                break
        except ValueError:
            print("Некорректный ввод. Введите число.")

    rooms = []
    for room_num in range(1, room_count + 1):
        while True:
            try:
                adults_count = int(input(f"Комната {room_num}: Введите количество взрослых: "))
                if not (1 <= adults_count <= 4):
                    print("Количество взрослых должно быть не менее 1 и не больше 4.")
                    continue

                children_count = int(input(f"Комната {room_num}: Введите количество детей: "))
                if not (0 <= children_count <= 4):
                    print("Количество взрослых должно быть не менее 0 и не больше 4.")
                    continue

                children_ages = []
                for child_num in range(1, children_count + 1):
                    while True:
                        try:
                            age = int(input(f"Комната {room_num}, ребенок {child_num}: Введите возраст ребенка: "))
                            if not (0 <= age <= 17):
                                print("Возраст детей должен быть от 0 до 17 лет.")
                                continue
                            children_ages.append({"age": age})
                            break
                        except ValueError:
                            print("Некорректный ввод. Введите число.")

                room = {"adults": adults_count, "children": children_ages}
                rooms.append(room)
                break
            except ValueError:
                print("Некорректный ввод. Введите число.")

    return rooms


def get_city_id() -> int:
    """
    Запрашивает название города и возвращает ID города, в котором находится отель.

    Returns:
        :return city id
        :rtype int
    """

    while True:
        try:
            city = input("\nВведите город, в котором находится отель: ").lower()
            city_id = get_city(url=url, headers=headers, city_name=city)

            if city_id:
                break
            else:
                print('Такого города не найдено!')
                continue
        except IndexError:
            print('Такого города не найдено!')

    return city_id


def get_user_datas() -> list:

    """
    Запрашивает данные у пользователя, необходимые для выбора отеля.
    Делает валидацию данных.

    Returns:
        :return (arrival date, departure date, room data and city ID).
        :rtype list
    """

    get_info()
    check_in_date, check_out_date = get_datas()
    rooms = get_rooms()
    city_id = get_city_id()

    return [check_in_date, check_out_date, rooms, city_id]
