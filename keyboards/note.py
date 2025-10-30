from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


note_action = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Удалить 🗑",
                callback_data="remove_note"
            ),
            InlineKeyboardButton(
                text="Назад",
                callback_data="BACK"
            )
        ]
    ]
)

back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="BACK"
            )
        ]
    ]
)
