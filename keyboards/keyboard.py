from typing import List
from datetime import datetime as dt, UTC

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import BACK, BAX, YENA, EURO, SOM


# The keyboard is used to cancel an action.
cancel_button: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="current")]
    ]
)

# Keyboard to confirm the deletion.
confirm_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="current"),
            InlineKeyboardButton(text="Продолжить", callback_data="continue"),
        ]
    ]
)

# The back button to return to the calendar information.
back: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Кал-рь 📅", callback_data="current"
            )
        ]
    ]
)

# The back button to return to the information for the month.
back_calendar = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔙",
                        callback_data="calendar"
                    )
                ]
            ]
        )


async def back_to_information(
    next_: bool,
    prev: bool
) -> InlineKeyboardMarkup:
    """
    The back button to return to the information for the month.
    
    :param next_: Is there another transaction.
    :param prev: Whether there are any previous entries.
    """
    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=BACK, callback_data="calendar"),
            InlineKeyboardButton(text="календарь", callback_data="current")
        ],
        [
            InlineKeyboardButton(
                text="Удалить запись",
                callback_data="remove_transaction"
            )
        ]
    ]
    if next_:
        buttons[0].append(
            InlineKeyboardButton(text=">>", callback_data="next_tr")
        )
    if prev:
        buttons[0].insert(
            0,
            InlineKeyboardButton(text="<<", callback_data="prev_tr")
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def next_prev_year(year) -> InlineKeyboardMarkup:
    """
    Generate a keyboard for working with statistics for the year.
    
    :param year: A year for statistics.
    """
    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=BAX,
                callback_data="dollar_y"
            ),
            InlineKeyboardButton(
                text=EURO,
                callback_data="euro_y"
            ),
            InlineKeyboardButton(
                text=YENA,
                callback_data="yena_y"
            ),
            InlineKeyboardButton(
                text=SOM,
                callback_data="som_y"
            )
        ],
        [
            InlineKeyboardButton(
                text="<<",
                callback_data="prev_year",
            ),
            InlineKeyboardButton(
                text="Календарь",
                callback_data="current"
            )
        ]
    ]
    if year < dt.now(UTC).year:
        buttons[1].append(
            InlineKeyboardButton(
                text=">>",
                callback_data="next_year"
            )
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
