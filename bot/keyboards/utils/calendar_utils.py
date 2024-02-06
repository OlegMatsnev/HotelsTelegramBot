from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
from datetime import datetime as dtm
from datetime import timedelta
import calendar


def is_available_next_month(year, month):
    current_year = Calendar.current_year
    current_month = Calendar.current_month

    if year == current_year:
        pass
    elif year == current_year + 1:
        month += 12
    elif year == current_year + 2:
        month += 24
    return (month - current_month) <= 16


def prev_next_month_button(year, month, markup: InlineKeyboardMarkup):
    prev_month_button = InlineKeyboardButton("Предыдущий месяц")
    next_month_button = InlineKeyboardButton("Следующий месяц")

    current_year = Calendar.current_year
    current_month = Calendar.current_month

    if current_year == year and current_month == month:
        # if we have starting month we can't move a left to prev month
        prev_month_button.callback_data = "empty"

        # update next month counter
        if current_month == 12:
            next_month_button.callback_data = f"arrival_data_{year + 1}_{1}"
        else:
            next_month_button.callback_data = f"arrival_data_{year}_{month + 1}"

    elif not is_available_next_month(year, month):
        # if we have last available month we can't move right to a next month
        next_month_button.callback_data = "empty"

        if current_month == 1:
            prev_month_button.callback_data = f"arrival_data_{year - 1}_{12}"
        else:
            prev_month_button.callback_data = f"arrival_data_{year}_{month - 1}"

    else:
        if month == 1:
            prev_month_button.callback_data = f"arrival_data_{year - 1}_{12}"
            next_month_button.callback_data = f"arrival_data_{year}_{month + 1}"
        elif month == 12:
            prev_month_button.callback_data = f"arrival_data_{year}_{month - 1}"
            next_month_button.callback_data = f"arrival_data_{year + 1}_{1}"
        else:
            prev_month_button.callback_data = f"arrival_data_{year}_{month - 1}"
            next_month_button.callback_data = f"arrival_data_{year}_{month + 1}"

    markup.row(prev_month_button, next_month_button)
    return markup


def first_row(year, month_num, markup: InlineKeyboardMarkup):
    months = ['Январь', 'Февраль', 'Март',
              'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь',
              'Октябрь', 'Ноябрь', 'Декабрь']

    month_name = months[month_num - 1]
    month_year_button_text = f"{month_name} {year}"

    month_year_button = InlineKeyboardButton(month_year_button_text, callback_data="empty")
    markup.row(month_year_button)
    return markup


def call_arrival_month_calendar(year, month, markup: InlineKeyboardMarkup):
    current_year = Calendar.current_year
    current_month = Calendar.current_month

    if current_year == year and current_month == month:
        markup = Calendar.get_curr_month_days_keyboard(markup=markup)
    else:
        markup = get_any_month_days_keyboard(year=year, month=month, markup=markup)

    return markup


def call_departure_start_month_calendar(start_day, start_month, start_year,
                                        markup: InlineKeyboardMarkup, first_month_days=None):
    if not first_month_days:
        first_month_days = get_month_days(year=start_year, month=start_month)
    markup = Calendar.get_curr_month_days_keyboard(markup=markup,
                                                   year=start_year,
                                                   month=start_month,
                                                   day=start_day,
                                                   days_in_month=first_month_days, dep_or_arrive_str="departure")
    return markup


def call_departure_last_month_calendar(last_day, last_month, last_year, markup: InlineKeyboardMarkup):
    markup = get_any_month_days_keyboard(markup=markup, year=last_year, month=last_month, days_in_month=last_day,
                                         dep_or_arrive_str="departure")
    return markup


def second_row(markup: InlineKeyboardMarkup()):
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    buttons_list = [InlineKeyboardButton(day, callback_data="empty") for day in weekdays]
    markup.row(*buttons_list)
    # Добавляем ряд с днями недели
    return markup


def get_month_days(year, month):
    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])
    days_in_month = (last_day - first_day).days + 1
    return days_in_month


def get_any_month_days_keyboard(year, month, markup, dep_or_arrive_str="arrival", days_in_month=None):
    current_weekday = calendar.weekday(year, month, 1)  # номер дня недели первого числа
    current_day = 1
    if not days_in_month:
        days_in_month = get_month_days(year, month)
    row_buttons_lst = []

    # fill cells by empty buttons for days before first month day
    for _ in range(current_weekday):
        row_buttons_lst.append(InlineKeyboardButton("\u200B", callback_data="empty"))

    last_empty_buttons_num = 0

    while current_day <= days_in_month:
        while current_weekday < 7:
            if current_day > days_in_month:
                last_empty_buttons_num = 7 - current_weekday
                break
            row_buttons_lst.append(InlineKeyboardButton(
                str(current_day), callback_data=f'{dep_or_arrive_str}_year_{year}_month_{month}_day_{str(current_day)}'))
            current_day += 1
            current_weekday += 1

        if last_empty_buttons_num != 0:
            break
        markup.row(*row_buttons_lst)
        row_buttons_lst = []
        current_weekday = 0

    # fill cells by empty buttons for days after last month day
    for _ in range(last_empty_buttons_num):
        row_buttons_lst.append(InlineKeyboardButton("\u200B", callback_data="empty"))
    markup.row(*row_buttons_lst)
    return markup


def get_next_last_data(year: int, month: int, day: int, next_day=1) -> tuple[int, int, int]:
    current_date = dtm(year, month, day)
    next_date = current_date + timedelta(days=next_day)
    return next_date.day, next_date.month, next_date.year


def get_date_caption(user_input_date: dict):
    months = ['Января', 'Февраля', 'Марта',
              'Апреля', 'Мая', 'Июня',
              'Июля', 'Августа', 'Сентября',
              'Октября', 'Ноября', 'Декабря']

    arrive_month_num = user_input_date["checkInDate"]["month"]
    arrive_month_info = months[arrive_month_num - 1]
    departure_month_num = user_input_date["checkOutDate"]["month"]
    departure_month_info = months[departure_month_num - 1]

    arrive_date_info = f'Дата прибытия: {user_input_date["checkInDate"]["day"]} ' \
                       f'{arrive_month_info} ' \
                       f'{user_input_date["checkInDate"]["year"]}'
    departure_date_info = f'Дата отбытия: {user_input_date["checkOutDate"]["day"]} ' \
                          f'{departure_month_info} ' \
                          f'{user_input_date["checkOutDate"]["year"]}'

    return arrive_date_info + "\n" + departure_date_info


class Calendar:
    now = dtm.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    @staticmethod
    def get_curr_month_days_keyboard(markup: InlineKeyboardMarkup(), dep_or_arrive_str="arrival",
                                     year=None, month=None, day=None, days_in_month=None):
        # for departure data we need to have additional parameters
        # so due to this we calc needed data
        if not year:
            current_year = Calendar.current_year
            current_month = Calendar.current_month
            current_day = Calendar.current_day

            # calculate days in current month
            days_in_month = get_month_days(current_year, current_month)
        else:
            current_year = year
            current_month = month
            current_day = day



        # calendar will get data input only starting with next day of current
        start_day = current_day + 1

        # getting weekday num we will start with
        date = datetime.date(current_year, current_month, start_day)  # full curr data info
        day_of_week_number = date.weekday()  # current weekday

        # Firstly we will work with the first row of our calendar,
        # so let's calc first not empty days
        days_in_first_row = 7 - day_of_week_number

        # fill first row

        row_buttons_lst = []
        for weekday_i in range(7):
            # we must check our day number:
            current_day_number = start_day - day_of_week_number + weekday_i

            # if our first row equals last month week -> we have to leave this circle
            if current_day_number > days_in_month:
                break

            # cells (buttons) which are being before starting day (day_of_week_number) will be empty
            if weekday_i < day_of_week_number:
                row_buttons_lst.append(InlineKeyboardButton("\u200B", callback_data="empty"))
            # other cells will have their day number in calendar
            else:
                row_buttons_lst.append(InlineKeyboardButton(str(current_day_number),
                                                            callback_data=f'{dep_or_arrive_str}_year_{current_year}_month_{current_month}_day_{str(current_day_number)}'))
        markup.row(*row_buttons_lst)
        # if our first row will not last month week -> we successfully filled it.

        # Next step -> fill other rows
        # Now we will get rows num of our curr month,
        # for this calc days (without first row days and days before this row) and divide by 7
        # (add up 1 due to // division,
        # for example for 8 days: 8 // 7 == 1, but we need to add second row, so add up with 1 our result)
        rows_count = ((days_in_month - days_in_first_row - (
                start_day - 1)) // 7) + 1

        row_buttons_lst = []
        for row_i in range(rows_count):
            first_weekday = start_day + days_in_first_row + (7 * row_i)
            for weekday_i in range(7):
                cur_day_i = weekday_i + first_weekday
                if cur_day_i <= days_in_month:
                    row_buttons_lst.append(InlineKeyboardButton(str(cur_day_i),
                                                                callback_data=f'{dep_or_arrive_str}_year_{current_year}_month_{current_month}_day_{str(cur_day_i)}'))
                else:
                    row_buttons_lst.append(InlineKeyboardButton("\u200B", callback_data="empty"))
            markup.row(*row_buttons_lst)
            row_buttons_lst = []

        return markup


