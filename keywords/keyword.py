from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cancel: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

confirm: List[List[InlineKeyboardButton]] = [
    [
        InlineKeyboardButton(text="Отмена", callback_data="main"),
        InlineKeyboardButton(text="Продолжить", callback_data="continue"),
    ]
]

menu_button: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=f"Календарь", callback_data="month_current"
            ),
            InlineKeyboardButton(text="Прогноз", callback_data="prediction"),
            InlineKeyboardButton(text="Настройки", callback_data="settings"),
        ],
        [
            InlineKeyboardButton(
                text="Проставить смены", callback_data="many_add"
            ),
            InlineKeyboardButton(
                text="Статистика за год", callback_data="statistic"
            ),
        ],
    ]


cancel_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=cancel)
confirm_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=confirm)
menu: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=menu_button)
