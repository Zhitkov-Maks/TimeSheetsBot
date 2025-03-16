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
            InlineKeyboardButton(text="📆", callback_data="month_current"),
            InlineKeyboardButton(text="⚙️", callback_data="settings"),
            InlineKeyboardButton(text="🛠", callback_data="many_add"),
            InlineKeyboardButton(text="↗", callback_data="statistic"),
        ]
    ]


cancel_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=cancel
)
confirm_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=confirm
)
menu: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=menu_button)
