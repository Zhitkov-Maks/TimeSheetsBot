from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import BACK, MENU, BAX, EURO, YENA, SOM


async def get_data_choices_day(salary: dict) -> InlineKeyboardMarkup:
    """
    Generate a keyboard to display data for a specific day.

    :param salary: A dictionary containing salary information.
    :return: An inline keyboard with buttons for user interaction.
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
                [
                  InlineKeyboardButton(
                      text=BAX,
                      callback_data="dollar"
                  ),
                  InlineKeyboardButton(
                      text=EURO,
                      callback_data="euro"
                  ),
                  InlineKeyboardButton(
                      text=YENA,
                      callback_data="yena"
                  ),
                  InlineKeyboardButton(
                      text=SOM,
                      callback_data="som"
                  )
                ],
                [
                    InlineKeyboardButton(
                        text="+ 📝",
                        callback_data="add_note"
                    ),
                    InlineKeyboardButton(
                        text="💵",
                        callback_data="award"
                    ),
                    InlineKeyboardButton(
                        text="👀 📝",
                        callback_data="show_note"
                    )
                ]
            ]
        )
