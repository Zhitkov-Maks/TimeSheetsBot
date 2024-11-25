from datetime import timedelta, datetime as dt
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keywords.keyword import month_tuple


def prediction_button() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=f"{month_tuple[dt.now().month]}/Посчитать",
                callback_data="current",
            ),
            InlineKeyboardButton(
                text=f"{month_tuple[(dt.now() + timedelta(days=30)).month]}/Посчитать",
                callback_data="next_month",
            ),
        ]
    ]


async def prediction() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=prediction_button())


select_schedule_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="График 5/2", callback_data="five_days"),
        InlineKeyboardButton(text="График 2/2", callback_data="two_in_two")
    ]
]

select_schedule_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=select_schedule_button)


delay_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Да Вт/Чт/2ч", callback_data="2/2"),
        InlineKeyboardButton(text="Да Вт/Чт/3ч", callback_data="2/3"),
        InlineKeyboardButton(text="Да Пн-Ср/3ч", callback_data="3/3"),
    ],
    [
        InlineKeyboardButton(text="Нет", callback_data="delay_no"),
        InlineKeyboardButton(text="Отмена", callback_data="main"),
    ]
]

delay_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=delay_button)
