from datetime import datetime as dt

from aiogram.types import KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


month_tuple = (
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
)

year_list = [
    [
        KeyboardButton(text=str(dt.now().year - 2)),
        KeyboardButton(text=str(dt.now().year - 1)),
        KeyboardButton(text=str(dt.now().year)),
    ]
]

month_list = [
    [
        KeyboardButton(text="Январь"),
        KeyboardButton(text="Февраль"),
        KeyboardButton(text="Март"),
        KeyboardButton(text="Апрель"),
    ],
    [
        KeyboardButton(text="Май"),
        KeyboardButton(text="Июнь"),
        KeyboardButton(text="Июль"),
        KeyboardButton(text="Август")
    ],
    [
        KeyboardButton(text="Сентябрь"),
        KeyboardButton(text="Октябрь"),
        KeyboardButton(text="Ноябрь"),
        KeyboardButton(text="Декабрь")
    ]
]

select_keyboard = [
    [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
]

reset_to_zero = [
    [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
]

menu_bot = [
    [
        InlineKeyboardButton(
            text=f"{month_tuple[dt.now().month - 1]}/Посмотреть",
            callback_data="month_current"
        ),
        InlineKeyboardButton(
            text=f"{month_tuple[dt.now().month - 2]}/Посмотреть",
            callback_data="month_prev"
        )],
    [
        InlineKeyboardButton(
            text="Добавить доход", callback_data="select_date"
        ),
        InlineKeyboardButton(
            text="Заработано за...", callback_data="period"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Калькулятор", callback_data="calc"
        ),
        InlineKeyboardButton(
            text="Сегодня", callback_data="today"
        ),
    ]
]

confirm = [
    [InlineKeyboardButton(
        text="Отмена",
        callback_data="main"
    ),
        InlineKeyboardButton(
            text="Продолжить",
            callback_data="continue"
        )]
]

mail = [
    [
        InlineKeyboardButton(
            text="Мой телеграм",
            url='tg://resolve?domain=Maksim1Zhitkov'
        ),
        InlineKeyboardButton(
            text="Закрыть",
            callback_data="main"
        )
    ]
]

cancel = [
    [InlineKeyboardButton(text="Отмена", callback_data="main")]
]

cancel_button = InlineKeyboardMarkup(inline_keyboard=cancel)
confirm_menu = InlineKeyboardMarkup(inline_keyboard=confirm)
mail_menu = InlineKeyboardMarkup(inline_keyboard=mail)
menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
