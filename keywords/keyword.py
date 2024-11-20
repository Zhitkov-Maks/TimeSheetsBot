from datetime import datetime as dt
from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg.pgproto.pgproto import timedelta

from database.models import Salary

month_tuple: Dict[int, str] = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

month_data: tuple = (
    "january",
    "february",
    "mart",
    "april",
    "mai",
    "june",
    "july",
    "august",
    "september",
    "oktober",
    "november",
    "december",
)

cancel: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

confirm: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Отмена", callback_data="main"),
        InlineKeyboardButton(text="Продолжить", callback_data="continue"),
    ]
]

confirm_two: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        InlineKeyboardButton(text="Продолжить", callback_data="continue"),
    ]
]

choice_remind: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Добавить", callback_data="add_remind"),
        InlineKeyboardButton(text="Удалить", callback_data="remove"),
    ],
    [
        InlineKeyboardButton(text="Изменить время", callback_data="change_remind"),
        InlineKeyboardButton(text="Отмена", callback_data="main"),
    ],
]


confirm_button: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Да", callback_data="yes"),
        InlineKeyboardButton(text="Нет", callback_data="main"),
    ]
]


def get_menu_bot() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(text=f"Календарь", callback_data="month_current"),
            InlineKeyboardButton(text="Калькулятор", callback_data="calc"),
            InlineKeyboardButton(text="Настройки", callback_data="settings"),
        ],
        [
            InlineKeyboardButton(text="Напоминание", callback_data="remind"),
            InlineKeyboardButton(text="Статистика за год", callback_data="statistic"),
        ],
    ]


def prediction_button() -> List[List[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton(
                text=f"{month_tuple[dt.now().month]}/Посчитать",
                callback_data="current_prediction",
            ),
            InlineKeyboardButton(
                text=f"{month_tuple[(dt.now() + timedelta(days=30)).month]}/Посчитать",
                callback_data="next_prediction",
            ),
        ]
    ]


async def prediction() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=prediction_button())


async def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=get_menu_bot())


async def get_data_choices_day(salary: Salary) -> InlineKeyboardMarkup:
    if not salary:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Меню", callback_data="main"),
                    InlineKeyboardButton(text="Добавить", callback_data="add"),
                ]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Меню", callback_data="main"),
                    InlineKeyboardButton(text="Изменить", callback_data="change"),
                ]
            ]
        )


cancel_button: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=cancel)
confirm_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=confirm)
confirm_menu_two: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=confirm_two
)
remind_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=choice_remind
)
