from collections import defaultdict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import MENU

# Possible settings for the user.
SETTINGS: dict[str, str] = {
    "price_time": "Ставка в час",
    "price_overtime": "Доплата за переработку",
    "price_cold": "Надбавка за холод",
    "price_award": "Стоимость операции"
}

settings_choices: dict[int, dict] = defaultdict(dict)


async def get_actions(user_id: int) -> InlineKeyboardMarkup:
    """
    Generate an inline keyboard to select settings.

    :param user_id: The telegram user's ID.
    :return InlineKeyboardMarkup: The inline keyboard.
    """
    keyboard: list[list[InlineKeyboardButton]] = [[]]
    for action in SETTINGS:
        # Adding a status button
        button_text = f"{SETTINGS[action]}    [✘] " \
            if action not in settings_choices[user_id] \
            else f"{SETTINGS[action]}    [✔️]"
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"toggle-{action}")
            ]
        )

    keyboard.append([
        InlineKeyboardButton(text="🆗", callback_data="finish"),
        InlineKeyboardButton(text="📅", callback_data="current"),
        InlineKeyboardButton(text="❌", callback_data="remove_settings")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
