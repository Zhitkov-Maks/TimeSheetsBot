from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import BACK, MENU


async def get_data_choices_day(salary) -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-клавиатуру на основе наличия данных о зарплате.

    :param salary: Словарь, содержащий информацию о зарплате.
    :return: Инлайн-клавиатура с кнопками для взаимодействия с пользователем.
    """
    if not salary:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="➕", callback_data="add"),
                    InlineKeyboardButton(text=MENU, callback_data="main"),
                    InlineKeyboardButton(
                        text=BACK, callback_data="current"
                    )
                ],
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✘", callback_data="del"),
                    InlineKeyboardButton(text=MENU, callback_data="main"),
                    InlineKeyboardButton(text="✍", callback_data="change"),
                    InlineKeyboardButton(
                        text=BACK, callback_data="current"
                    )
                ],
            ]
        )
