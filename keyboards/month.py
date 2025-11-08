from calendar import monthrange
from datetime import date, datetime as dt
from typing import Dict, List, Tuple

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import (
    UNICODE_DATA,
    MONTH_DATA,
    DAYS_LIST,
    MENU,
    BACK,
    BAX,
    EURO,
    YENA,
    SOM
)


async def get_dates(salary) -> Dict[str, int]:
    """
    Create a dictionary where the key is the date and the 
    value is the number of hours worked for the selected date.

    :param salary: The result of the database query.
    :return Dict: A dictionary with dates and hours worked.
    """
    return {
        sal.get("date").strftime("%Y-%m-%d"): sal.get("base_hours")
        for sal in salary
    }


async def create_list_with_calendar_days(
    day_week: int,
    days_in_month: int,
    days: int
) -> List[str]:
    """
    Create a list with calendar days, 
    plus empty cells before the first day, 
    plus empty cells after the last day of the month.

    :param day_week: The number of the day of the 
                        week is the first of the month.
    :param days_in_month: There are only days in a month.
    :param days: The size of the calendar field.
    :return List: A list with a calendar field.
    """
    return (
            [" "] * day_week
            + [f"{i:02}" for i in range(1, days_in_month + 1)]
            + [" "] * (days - days_in_month - day_week)
            )


async def generate_base_calendar(
    field_size: int,
    numbers_list: List[str],
    dates: Dict[str, int],
    month_keyword: list,
    year: int,
    month: int
) -> None:
    """
    Generate a calendar displaying work shifts.

    :param field_size: The size of the calendar field.
    :param numbers_list: The calendar field.
    :param dates: A dictionary with dates and earnings.
    :param month_keyword: The keyboard itself is in the form of a calendar.
    :param year: Year for generate the date.
    :param month: A month for forming the date.
    :return List: The inline keyboard.
    """
    current_date = str(dt.now().date())
    for i in range(7):  # For each day of the week (7 days)
        row: List[InlineKeyboardButton] = [
            InlineKeyboardButton(text=DAYS_LIST[i], callback_data=DAYS_LIST[i])
        ]
        day = i

        # For each row in the field (depending on the size)
        for _ in range(field_size):
            create_date: str = f"{year}-{month:02}-{numbers_list[day]}"

            if numbers_list[day] == " ":
                text = " "

            elif create_date in dates:
                text = f"{numbers_list[day]} {UNICODE_DATA[dates[create_date]]}"

            else:
                text = f"({numbers_list[day]})"

            row.append(
                InlineKeyboardButton(text=text, callback_data=create_date)
            )
            day += 7

        month_keyword.append(row)


async def create_calendar(
        salary,
        year: int,
        month: int,
        data: tuple[tuple]
) -> InlineKeyboardMarkup:
    """
    Генерирует календарь за указанный месяц.

    :param salary: Результат запроса в БД за переданный месяц.
    :param year: Год для отображения в календаре.
    :param month: Месяц для отображения в календаре.

    :return: Инлайн клавиатура с днями месяца и соответствующими
        данными о зарплате.
    """

    # Создание словаря с датами и количеством отработанных часов
    dates: Dict[str, int] = await get_dates(salary)
    
    # Получение дня недели 1 числа месяца и количества дней в месяце.
    day_week: int = date(year, month, 1).weekday()
    days_in_month: int = monthrange(year, month)[1]

    # Инициализация списка для инлайн-клавиатуры
    month_keyword: List[List[InlineKeyboardButton]] = []

    # Определение размера поля и количества дней для отображения
    field_size, days = await get_month_range(day_week, days_in_month)

    # Формирование списка номеров дней с учетом пустых ячеек
    numbers_list: List[str] = await create_list_with_calendar_days(
        day_week, days_in_month, days
    )

    # Формирование строк с днями недели и их значениями
    await generate_base_calendar(
        field_size, numbers_list, dates, month_keyword, year, month
    )
    
    # Добавление информации о зп за периоды.
    month_keyword.append(
        [
            InlineKeyboardButton(
                text=f"{data[0][0]:,}₽/{data[0][1]}ч",
                callback_data="period1"
            ),
            InlineKeyboardButton(
                text=f"{data[1][0]:,}₽/{data[1][1]}ч",
                callback_data="period2"
            ),
        ]
    )

    # Добавление кнопок навигации внизу календаря
    month_keyword.append(
        [
            InlineKeyboardButton(
                text=f"Итого: {data[2][0]:,}₽ / {data[2][1]}ч.",
                callback_data="total_amount"
            )
        ]
    )
    
    # Добавление заголовка месяца в клавиатуру
    month_keyword.append(
        [   InlineKeyboardButton(text="<<", callback_data="prev"),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[month]} {year}г",
                callback_data="calendar"
            ),
            InlineKeyboardButton(text=">>", callback_data="next"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=month_keyword)


async def get_month_range(
        day_week: int, days_in_month: int
) -> Tuple[int, int]:
    """
    Определяет размер поля и количество дней для отображения в календаре
    на основе дня недели и количества дней в месяце.

    :param day_week: Целое число, представляющее день недели (0 - понедельник,
                        6 - воскресенье).
    :param days_in_month: Общее количество дней в месяце.

    :return: Кортеж из двух целых чисел:
             - field_size: Размер поля для отображения (4, 5 или 6).
             - days: Общее количество дней для отображения (28, 35 или 42).
    """
    field_size: int = 5
    days: int = 35

    # Проверка, если общее количество дней в месяце и день недели превышает 35
    if day_week + days_in_month > 35:
        field_size = 6
        days = 42

    # Проверка, если общее количество дней в месяце и день недели меньше 29
    elif days_in_month + day_week < 29:
        field_size = 4
        days = 28

    return field_size, days


async def get_month_menu() -> InlineKeyboardMarkup:
    """
    Turn back the keyboard to select actions when 
    displaying information for the month.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="+",
                    callback_data="other_income"
                ),

                InlineKeyboardButton(
                    text="📈",
                    callback_data="list_incomes"
                ),
                InlineKeyboardButton(
                    text="📉",
                    callback_data="list_expenses"
                ),
                InlineKeyboardButton(
                    text="📆",
                    callback_data="current"
                ),
                InlineKeyboardButton(
                    text="-",
                    callback_data="expences"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=BAX,
                    callback_data="dollar_m"
                ),
                InlineKeyboardButton(
                    text=EURO,
                    callback_data="euro_m"
                ),
                InlineKeyboardButton(
                    text=BACK,
                    callback_data="current"
                ),
                InlineKeyboardButton(
                    text=YENA,
                    callback_data="yena_m"
                ),
                InlineKeyboardButton(
                    text=SOM,
                    callback_data="som_m"
                )
            ]
        ]
    )
