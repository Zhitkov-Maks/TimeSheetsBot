from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import BACK


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
            InlineKeyboardButton(text="🛠", callback_data="many_add")
        ],
        [
            InlineKeyboardButton(
                text="Курсы валют",
                callback_data="valute"
            )
        ]
    ]


cancel_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=cancel
)
confirm_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=confirm
)

menu: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=menu_button)

back: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад 🔙", callback_data="main"
            ),
            InlineKeyboardButton(
                text="Кал-рь 📅", callback_data="month_current"
            )
        ]
    ]
)


async def back_to_information() -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=BACK, callback_data="calendar"),
            InlineKeyboardButton(text="Меню", callback_data="main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
