from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Keyboard when working with notes.
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

# The back button when working with notes.
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
