from calendar import monthrange
from datetime import date, datetime as dt, timedelta
from typing import List
from collections import defaultdict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.month import get_month_range, create_list_with_calendar_days
from loader import MONTH_DATA, DAYS_LIST

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
    Fill the calendar with buttons.
    
    :param field_size: The size of the calendar field.
    :param numbers_list: The calendar field.
    :param month_keyword: The keyboard itself is in the form of a calendar.
    :param year: The selected year.
    :param user_chat_id: The user's ID.
    :param month: The selected month.
    :return List: The inline keyboard.
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
                text = f"{numbers_list[day]} ○" \
                    if create_date not in days_choices[user_chat_id] \
                    else f"{numbers_list[day]} ●"

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
    Add the main buttons to the calendar.
    
    :param year: The year for the calendar.
    :param month: The month for the calendar.
    :param user_chat_id: The ID of the chat user.
    :return InlineKeyboardMarkup: An inline keyboard in the form of a calendar.
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
        InlineKeyboardButton(text="📅", callback_data="current")
    ])
    return InlineKeyboardMarkup(inline_keyboard=month_keyword)


async def next_month_date(days, year, month) -> str:
    """
    Get the next month.
    
    :param days: The number of days to add.
    :param year: The transmitted year.
    :param month: The transmitted month.
    """
    return (
        f"{(date(year, month, 1) + timedelta(days=days)).year}-"
        f"{(date(year, month, 1) + timedelta(days=days)).month}"
    )


async def prediction_button() -> InlineKeyboardMarkup:
    """
    Generate inline buttons to select the current and next month.

    :return: The inline keyboard.
    """
    year, month = dt.now().year, dt.now().month
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{MONTH_DATA[dt.now().month]}",
                callback_data=f"{dt.now().year}-{dt.now().month}",
            ),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=35)).month]}",
                callback_data=await next_month_date(35, year, month),
            ),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=65)).month]}",
                callback_data=await next_month_date(65, year, month),
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=96)).month]}",
                callback_data=await next_month_date(96, year, month),
            ),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=126)).month]}",
                callback_data=await next_month_date(126, year, month),
            ),
            InlineKeyboardButton(
                text=f"{MONTH_DATA[(
                        date(year, month, 1) + timedelta(days=157)).month]}",
                callback_data=await next_month_date(156, year, month),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Календарь",
                callback_data="current"
            ),
        ]
    ])
