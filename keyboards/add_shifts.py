from calendar import monthrange
from datetime import date, datetime as dt, timedelta
from typing import List
from collections import defaultdict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.month import get_month_range, create_list_with_calendar_days
from loader import MONTH_DATA, DAYS_LIST, MENU

days_choices = defaultdict(set)


async def generate_base_calendar(
        field_size: int,
        numbers_list: List[str],
        month_keyword: list,
        year: int,
        month: int,
        user_chat_id: int
) -> None:
    """
    Функция генерации основной части календаря. Заполняет календарь кнопками.
    
    :param field_size: Размер поля календаря.
    :param numbers_list: Поле календаря.
    :param month_keyword: Непосредственно клавиатура в виде календаря.
    :param year: Нужен для формирования даты.
    :param user_chat_id: Нужен для формирования клавиатуры.
    :param month: Нужен для формирования даты.
    :return List: Инлайн клавиатуру.
    """
    for i in range(7):
        row: List[InlineKeyboardButton] = [InlineKeyboardButton(
            text=DAYS_LIST[i], callback_data=DAYS_LIST[i])]

        day = i
        for _ in range(field_size):
            create_date: str = f"{year}-{month:02}-{numbers_list[day]}"
            if numbers_list[day] == " ":
                text = " "
            else:
                text = f"{numbers_list[day]} ˟" \
                    if create_date not in days_choices[user_chat_id] \
                    else f"{numbers_list[day]} ˯"

            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"toggle2_{create_date}",
                )
            )
            day += 7
        month_keyword.append(row)


async def get_days_keyboard(
        year: int,
        month: int,
        user_chat_id: int
) -> InlineKeyboardMarkup:
    """
    Функция для генерации календаря для выбора смен, при групповой
    простановке смен.
    :param year: Год для календаря.
    :param month: Месяц для календаря.
    :param user_chat_id: Идентификатор пользователя чата.
    :return InlineKeyboardMarkup: Инлайн клавиатура в виде календаря.
    """
    days_in_month: int = monthrange(year, month)[1]
    day_week: int = date(year, month, 1).weekday()

    month_keyword: List[List[InlineKeyboardButton]] = []
    field_size, days = await get_month_range(day_week, days_in_month)

    numbers_list: List[str] = await create_list_with_calendar_days(
        day_week, days_in_month, days
    )

    month_keyword.append(
        [InlineKeyboardButton(
            text=f"{MONTH_DATA[month]} {year}г", callback_data="календарь"),])

    await generate_base_calendar(
        field_size, numbers_list, month_keyword, year, month, user_chat_id
    )

    month_keyword.append([
        InlineKeyboardButton(text="🆗", callback_data="shift_finish"),
        InlineKeyboardButton(text=MENU, callback_data="main"),
        InlineKeyboardButton(text="📅", callback_data="month_current")
    ])
    return InlineKeyboardMarkup(inline_keyboard=month_keyword)


async def prediction_button() -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-кнопки для выбора текущего и следующего месяца.

    :return: Инлайн клавиатуру.
    """
    year, month = dt.now().year, dt.now().month
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{MONTH_DATA[dt.now().month]}",
                callback_data="cur",
            ),
            InlineKeyboardButton(text=MENU, callback_data="main"),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=35)).month]}",
                callback_data="next_month",
            ),
        ]
    ])
