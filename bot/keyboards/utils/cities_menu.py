from telebot import types
from telebot.types import InlineKeyboardButton


def select_continent(callback):
    buttons_lst = [InlineKeyboardButton('Азия', callback_data='cont_Asia_country_China'),
                   InlineKeyboardButton('Европа', callback_data='cont_Europe_country_Italy'),
                   InlineKeyboardButton('Африка', callback_data='cont_Africa_country_Morocco'),
                   InlineKeyboardButton('Юж. Америка', callback_data='cont_SouthAmerica_country_Brazil'),
                   InlineKeyboardButton('Сев. Америка', callback_data='cont_NorthAmerica_country_USA'),
                   InlineKeyboardButton('Австралия', callback_data='cont_Australia_country_Australia')]

    i = 0
    for continent in buttons_lst:
        if callback.split('_')[1] == continent.callback_data.split('_')[1]:
            buttons_lst[i].text = '[' + buttons_lst[i].text + ']'
        i += 1

    return buttons_lst


def select_country(callback, countries_data):
    countries = []

    for i in countries_data:
        country_name = next(iter(i.keys()))
        country_callback = next(iter(i.values()))
        countries.append(InlineKeyboardButton(str(country_name), callback_data=str(country_callback)))

    i = 0
    for country in countries:
        if callback.split('_')[3] == country.callback_data.split('_')[3]:
            countries[i].text = '[' + countries[i].text + ']'
        i += 1

    return countries


def show_cities(cities_data, markup):
    for i in cities_data:
        city_name = next(iter(i.keys()))
        city_callback = next(iter(i.values()))
        markup.row(InlineKeyboardButton(str(city_name), callback_data=str(city_callback)))


def get_country(callback):
    markup = types.InlineKeyboardMarkup()

    callback_str = callback.data

    markup.row(InlineKeyboardButton('🌏 Континенты 🌎', callback_data="empty"))
    continents = select_continent(callback=callback_str)
    cont_asia = continents[0]
    cont_europa = continents[1]
    cont_africa = continents[2]
    cont_north_america = continents[3]
    cont_south_america = continents[4]
    cont_australia = continents[5]
    markup.row(cont_asia, cont_australia, cont_north_america)
    markup.row(cont_europa, cont_africa, cont_south_america)

    markup.row(InlineKeyboardButton('Страны', callback_data="empty"))

    if callback_str.split('_')[1] == "Europe":
        countries_data = [
            {"🇹🇷": "cont_Europe_country_Turkey"},
            {"🇪🇸": "cont_Europe_country_Spain"},
            {"🇮🇹": "cont_Europe_country_Italy"},
            {"🇬🇧": "cont_Europe_country_Britain"}]

        countries = select_country(callback=callback_str, countries_data=countries_data)
        markup.row(*countries)

        markup.row(InlineKeyboardButton('🌆 Города 🌆', callback_data="empty"))

        if callback_str.split('_')[3] == "Turkey":
            cities_data = [
                {"Белек": "city_Belek"},
                {"Анкара": "city_Ankara"},
                {"Анталья": "city_Antalya"},
                {"Стамбул": "city_Istanbul"}]

            show_cities(cities_data=cities_data, markup=markup)

        if callback_str.split('_')[3] == "Spain":
            cities_data = [
                {"Мадрид": "city_Madrid"},
                {"Барселона": "city_Barcelona"},
                {"Севилья": "city_Sevilla"},
                {"Валенсия": "city_Valencia"}]

            show_cities(cities_data=cities_data, markup=markup)

        if callback_str.split('_')[3] == "Italy":
            cities_data = [
                {"Турин": "city_Turin"},
                {"Рим": "city_Rome"},
                {"Неаполь": "city_Naples"}]

            show_cities(cities_data=cities_data, markup=markup)

        if callback_str.split('_')[3] == "Britain":
            cities_data = [
                {"Лондон": "city_London"},
                {"Манчестер": "city_Manchester"},
                {"Ливерпуль": "city_Liverpool"}]

            show_cities(cities_data=cities_data, markup=markup)

    elif callback_str.split('_')[1] == "NorthAmerica":
        countries_data = [
            {"🇺🇸": "cont_NorthAmerica_country_USA"},
            {"🇨🇦": "cont_NorthAmerica_country_Canada"},
            {"🇲🇽": "cont_NorthAmerica_country_Mexico"}]

        countries = select_country(callback=callback_str, countries_data=countries_data)
        markup.row(*countries)

        markup.row(InlineKeyboardButton('🌆 Города 🌆', callback_data="empty"))

        if callback_str.split('_')[3] == "USA":
            cities_data = [
                {"Нью Йорк": "city_New York"},
                {"Майами": "city_Miami"},
                {"Лос Анджелес": "city_Los Angeles"},
                {"Лас Вегас": "city_Las Vegas"}]

            show_cities(cities_data=cities_data, markup=markup)


        elif callback_str.split('_')[3] == "Canada":
            cities_data = [
                {"Торонто": "city_Toronto"},
                {"Оттава": "city_Ottawa"}]

            show_cities(cities_data=cities_data, markup=markup)


        elif callback_str.split('_')[3] == "Mexico":
            cities_data = [
                {"Мехико": "city_Mexico"},
                {"Пуэбла": "city_Puabla"}]

            show_cities(cities_data=cities_data, markup=markup)

    elif callback_str.split('_')[1] == "SouthAmerica":
        countries_data = [
            {"🇧🇷": "cont_SouthAmerica_country_Brazil"},
            {"🇦🇷": "cont_SouthAmerica_country_Argentina"},
            {"🇨🇱": "cont_SouthAmerica_country_Chile"}]

        countries = select_country(callback=callback_str, countries_data=countries_data)
        markup.row(*countries)

        markup.row(InlineKeyboardButton('🌆 Города 🌆', callback_data="empty"))

        if callback_str.split('_')[3] == "Brazil":
            cities_data = [
                {"Рио-де-Жанейро": "city_Rio de Janeiro"},
                {"Сан-Паулу": "city_Sao Paulo"},
                {"Салвадор": "city_Salvador"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "Argentina":
            cities_data = [
                {"Буэнос-Айрес": "city_Buenos Aires"},
                {"Сальта": "city_Salta"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "Chile":
            cities_data = [
                {"Сантьяго": "city_Santiago"},
                {"Арика": "city_Arika"}]

            show_cities(cities_data=cities_data, markup=markup)

    elif callback_str.split('_')[1] == "Asia":
        countries_data = [
            {"🇯🇵": "cont_Asia_country_Japan"},
            {"🇨🇳": "cont_Asia_country_China"},
            {"🇰🇷": "cont_Asia_country_SouthKorea"},
            {"🇮🇩": "cont_Asia_country_Indonesia"},
            {"🇹🇭": "cont_Asia_country_Thailand"}]

        countries = select_country(callback=callback_str, countries_data=countries_data)
        markup.row(*countries)

        markup.row(InlineKeyboardButton('🌆 Города 🌆', callback_data="empty"))

        if callback_str.split('_')[3] == "Japan":
            cities_data = [
                {"Токио": "city_Tokio"},
                {"Чиба": "city_Chiba"},
                {"Осака": "city_Osaka"},
                {"Киото": "city_Kyoto"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "China":
            cities_data = [
                {"Чунцин": "city_Chongqing"},
                {"Пекин": "city_Beijing"},
                {"Шанхай": "city_Shanghai"},
                {"Гуанчжоу": "city_Guangzhou"},
                {"Шэньчжэнь": "city_Shenzhen"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "SouthKorea":
            cities_data = [
                {"Сеул": "city_Seoul"},
                {"Андон": "city_Andong"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "Indonesia":
            cities_data = [
                {"Нуса Дуа": "city_Nusa dua"},
                {"Джакарта": "city_Jakarta"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "Thailand":
            cities_data = [
                {"Бангкок": "city_Bangkok"},
                {"Пхукет": "city_Phuket"}]

            show_cities(cities_data=cities_data, markup=markup)

    elif callback_str.split('_')[1] == "Africa":
        countries_data = [
            {"🇪🇬": "cont_Africa_country_Egypt"},
            {"🇹🇳": "cont_Africa_country_Tunisia"},
            {"🇲🇦": "cont_Africa_country_Morocco"}]

        countries = select_country(callback=callback_str, countries_data=countries_data)
        markup.row(*countries)

        markup.row(InlineKeyboardButton('🌆 Города 🌆', callback_data="empty"))

        if callback_str.split('_')[3] == "Egypt":
            cities_data = [
                {"Каир": "city_Cairo"},
                {"Хургада": "city_Hurghada"},
                {"Шарм-эль-Шейх": "city_Sharm El Sheikh"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "Tunisia":
            cities_data = [
                {"Тунис": "city_Tunis"},
                {"Хаммамет": "city_Hammamet"}]

            show_cities(cities_data=cities_data, markup=markup)

        elif callback_str.split('_')[3] == "Morocco":
            cities_data = [
                {"Марракеш": "city_Marrakech"},
                {"Фес": "city_Fes"}]

            show_cities(cities_data=cities_data, markup=markup)

    elif callback_str.split('_')[1] == "Australia":
        countries_data = [
            {"🇦🇺": "cont_Australia_country_Australia"}]

        countries = select_country(callback=callback_str, countries_data=countries_data)
        markup.row(*countries)

        markup.row(InlineKeyboardButton('🌆 Города 🌆', callback_data="empty"))

        if callback_str.split('_')[3] == "Australia":
            cities_data = [
                {"Сидней": "city_Sydney"},
                {"Мельбурн": "city_Melbourne"},
                {"Канберра": "city_Canberra"}]

            show_cities(cities_data=cities_data, markup=markup)

    back_button = InlineKeyboardButton("⬅ Назад", callback_data='adults_count_1')
    info_button = InlineKeyboardButton("Справка", callback_data='countries_info')
    markup.row(back_button, info_button)

    return markup




