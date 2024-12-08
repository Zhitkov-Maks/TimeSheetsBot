from aiogram.types import Message, InlineKeyboardMarkup


async def remove_inline_keyword(message: Message):
    """
    Функция для удаления инлайн клавиатуры.
    :param message: Сообщение у которого необходимо удалить клавиатуру.
    """
    if (message.reply_markup and
        isinstance(message.reply_markup, InlineKeyboardMarkup)):
        await message.delete_reply_markup()
