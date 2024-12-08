from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Salary


async def get_data_choices_day(salary: Salary) -> InlineKeyboardMarkup:
    """
    Генерирует инлайн-клавиатуру на основе наличия данных о зарплате.

    :param salary: Объект Salary, содержащий информацию о зарплате.
    :return: Инлайн-клавиатура с кнопками для взаимодействия с пользователем.
    """
    if not salary:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Меню", callback_data="main"),
                    InlineKeyboardButton(text="Добавить", callback_data="add"),
                ],
                [
                    InlineKeyboardButton(
                        text="Открыть календарь",
                        callback_data="month_current"
                    )
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
                        text="Добавить бонус.",
                        callback_data="bonus")
                ],
                [
                    InlineKeyboardButton(
                        text="Календарь",
                        callback_data="month_current"
                    )
                ]
            ]
        )
