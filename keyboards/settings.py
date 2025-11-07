from collections import defaultdict

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import MENU

# Возможные настройки для пользователя.
SETTINGS: dict[str, str] = {
    "price_time": "Ставка в час",
    "price_overtime": "Доплата за переработку",
    "price_cold": "Надбавка за холод",
    "price_award": "Стоимость операции"
}

settings_choices: dict[int, dict] = defaultdict(dict)


async def get_actions(user_id: int) -> InlineKeyboardMarkup:
    """
    Генерация инлайн клавиатуры для выбора настроек.

    :param user_id: Идентификатор пользователя телеграм.
    :return InlineKeyboardMarkup: Инлайн клавиатуру.
    """
    keyboard: list[list[InlineKeyboardButton]] = [[]]
    for action in SETTINGS:
        # Добавляем кнопку с состоянием
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
