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
            ),
            InlineKeyboardButton(
                text="Срок годности",
                callback_data="expiration_date"
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


async def back_to_information(next: bool, prev: bool) -> InlineKeyboardMarkup:
    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=BACK, callback_data="calendar"),
            InlineKeyboardButton(text="Меню", callback_data="main")
        ],
        [
            InlineKeyboardButton(
                text="Удалить запись",
                callback_data="remove_transaction"
            )
        ]
    ]
    if next:
        buttons[0].append(
            InlineKeyboardButton(text=">>", callback_data="next_tr")
        )
    if prev:
        buttons[0].insert(
            0,
            InlineKeyboardButton(text="<<", callback_data="prev_tr")
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
