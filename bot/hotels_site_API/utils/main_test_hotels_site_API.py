# Импортируем функцию get_user_datas для получения данных от пользователя
from userData import get_user_datas
# Импортируем функции high_low_datas и custom для выполнения команд по фильтрации и сортировке отелей
from bot.hotels_site_API.utils.comands.high_low_command import high_low_datas
from bot.hotels_site_API.utils.comands.custom_command import custom
# Импортируем класс Hotel для работы с объектами отелей
from bot.hotels_site_API.utils.hotel import Hotel


# Функция для вывода списка отелей
def print_hotels(hotels_list: list[Hotel]) -> None:
    for hotel in hotels_list:
        print(hotel, end='\n\n')


# Получаем данные от пользователя, такие как даты, количество комнат, идентификатор города и др.
data_list: list = get_user_datas()
result_list = []

# Запрашиваем у пользователя выбор одной из предоставленных команд (временная замена запросов из Telegram!)
chose_command: str = input('Выберете одну из представленных команд одну (high/low/custom/history)')

if chose_command == 'low':

    count_of_hotels = 5
    while True:
        try:
            count_of_hotels = int(input('Введите количество получаемых отелей (от 1 до 5): '))
            if 1 <= count_of_hotels <= 5:
                break
            else:
                print('Число не входит в диапазон или не является целым!')
        except (TypeError, ValueError):
            print('Неправильный ввод данных!')
            continue

    criteria = input('Выберите критерий для отбора отелей (price, score, distance): ')
    if criteria == 'price':
        result_list = high_low_datas(data_list, high_sort=False, count_hotels=count_of_hotels, is_price=True)
    if criteria == 'score':
        result_list = high_low_datas(data_list, high_sort=False, count_hotels=count_of_hotels, is_scores=True)
    if criteria == 'distance':
        result_list = high_low_datas(data_list, high_sort=False, count_hotels=count_of_hotels, is_distance=True)

    print_hotels(result_list)


if chose_command == 'high':

    count_of_hotels = 5
    while True:
        try:
            count_of_hotels = int(input('Введите количество получаемых отелей (от 1 до 5): '))
            if 1 <= count_of_hotels <= 5:
                break
            else:
                print('Число не входит в диапазон или не является целым!')
        except (TypeError, ValueError):
            print('Неправильный ввод данных!')
            continue

    criteria = input('Выберите критерий для отбора отелей (price, score, distance)')
    if criteria == 'price':
        result_list = high_low_datas(data_list, high_sort=True, count_hotels=count_of_hotels, is_price=True)
    if criteria == 'score':
        result_list = high_low_datas(data_list, high_sort=True, count_hotels=count_of_hotels, is_scores=True)
    if criteria == 'distance':
        result_list = high_low_datas(data_list, high_sort=True, count_hotels=count_of_hotels, is_distance=True)

    print_hotels(result_list)

if chose_command == 'custom':

    count_of_hotels = 5
    while True:
        try:
            count_of_hotels = int(input('Введите количество получаемых отелей (от 1 до 5): '))
            if 1 <= count_of_hotels <= 5:
                break
            else:
                print('Число не входит в диапазон или не является целым!')
        except (TypeError, ValueError):
            print('Неправильный ввод данных!')
            continue

    criteria = input('Выберите критерий для отбора отелей (price, stars, pool)')
    if criteria == 'price':
        result_list = custom(data_list, count_hotels=count_of_hotels, price_filter=True)
    if criteria == 'stars':
        result_list = custom(data_list, count_hotels=count_of_hotels, stars_filter=True)
    if criteria == 'pool':
        result_list = custom(data_list, count_hotels=count_of_hotels, pool_filter=True)

    print()
    print_hotels(result_list)


