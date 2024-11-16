from datetime import datetime as dt
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg.pgproto.pgproto import timedelta

month_tuple = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
    7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь",
    12: "Декабрь"
}

month_data = (
    "january", "february", "mart", "april", "mai", "june",
    "july", "august", "september", "oktober", "november", "december",
)

cancel = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

confirm: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(
        text="Отмена",
        callback_data="main"
    ),
        InlineKeyboardButton(
            text="Продолжить",
            callback_data="continue"
        )]
]

confirm_two: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(
        text="Отмена",
        callback_data="cancel"
    ),
        InlineKeyboardButton(
            text="Продолжить",
            callback_data="continue"
        )]
]


def get_year_date() -> tuple:
    return str(dt.now().year - 2), str(dt.now().year - 1), str(dt.now().year)


def get_year_list() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=str(dt.now().year - 2),
                callback_data=str(dt.now().year - 2)
            ),
            InlineKeyboardButton(
                text=str(dt.now().year - 1),
                callback_data=str(dt.now().year - 1)
            ),
            InlineKeyboardButton(
                text=str(dt.now().year),
                callback_data=str(dt.now().year)
            ),
        ]
    ]


def get_month_list() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(text="Январь", callback_data="january"),
            InlineKeyboardButton(text="Февраль", callback_data="february"),
            InlineKeyboardButton(text="Март", callback_data="mart"),
            InlineKeyboardButton(text="Апрель", callback_data="april"),
        ],
        [
            InlineKeyboardButton(text="Май", callback_data="mai"),
            InlineKeyboardButton(text="Июнь", callback_data="june"),
            InlineKeyboardButton(text="Июль", callback_data="july"),
            InlineKeyboardButton(text="Август", callback_data="august")
        ],
        [
            InlineKeyboardButton(text="Сентябрь", callback_data="september"),
            InlineKeyboardButton(text="Октябрь", callback_data="oktober"),
            InlineKeyboardButton(text="Ноябрь", callback_data="november"),
            InlineKeyboardButton(text="Декабрь", callback_data="december")
        ]
    ]


def get_menu_bot() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=f"Календарь",
                callback_data="month_current"
            ),
            InlineKeyboardButton(
                text="Калькулятор", callback_data="calc"
            ),
        ],
    ]


def prediction_button() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=f"{month_tuple[dt.now().month]}/Посчитать",
                callback_data="current_prediction"
            ),
            InlineKeyboardButton(
                text=f"{month_tuple[(dt.now() + timedelta(days=30)).month]}/Посчитать",
                callback_data="next_prediction"
            ),
        ]
    ]


async def prediction() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=prediction_button())


async def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=get_menu_bot())


async def year_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=get_year_list())


async def month_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=get_month_list())


async def get_data_choices_day() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить", callback_data="change"),
            InlineKeyboardButton(text="Меню", callback_data="main"),
            InlineKeyboardButton(text="Добавить", callback_data="add")
        ]
    ])


cancel_button = InlineKeyboardMarkup(inline_keyboard=cancel)
confirm_menu = InlineKeyboardMarkup(inline_keyboard=confirm)
confirm_menu_two = InlineKeyboardMarkup(inline_keyboard=confirm_two)
