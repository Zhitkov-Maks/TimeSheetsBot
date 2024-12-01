from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Salary


async def get_data_choices_day(salary: Salary) -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-клавиатуру на основе наличия данных о зарплате.

    :param salary: Объект Salary, содержащий информацию о зарплате.
                   Если объект отсутствует (None), отображаются кнопки для
                   навигации в меню.

    :return: Инлайн-клавиатура с кнопками для взаимодействия с пользователем.
             Если salary отсутствует, возвращает клавиатуру с кнопками
                "Меню" и "Добавить".
             Если salary присутствует, возвращает клавиатуру с кнопками
                "Удалить", "Меню", "Изменить" и "Добавить бонус".
    """
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
                    InlineKeyboardButton(text="Удалить", callback_data="del"),
                    InlineKeyboardButton(text="Меню", callback_data="main"),
                    InlineKeyboardButton(text="Изменить",
                                         callback_data="change"),
                ],
                [
                    InlineKeyboardButton(
                        text="Добавить бонус(доплаты, акции).",
                        callback_data="bonus")
                ]
            ]
        )
