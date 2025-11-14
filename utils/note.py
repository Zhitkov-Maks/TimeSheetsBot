from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from utils.current_day import gen_message_for_choice_day
from keyboards.current_day import get_data_choices_day


async def answer_after_operation(
    message: CallbackQuery | Message,
    current_day: dict,
    action: str
) -> None:
    """
    Generate a response to the user after adding the note.

    :param message: A message or CallbackQuery type object
    :param current_day: Information for the selected day.
    :param action: Description of what action was performed.
    """
    date = current_day.get("date").strftime('%Y-%m-%d')
    mess: str = await gen_message_for_choice_day(current_day, date)
    keyboard = await get_data_choices_day(current_day)
    
    if isinstance(message, Message):
        await message.answer(
            text=hbold(f"{action} \n {mess}"),
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await message.message.edit_text(
            text=hbold(f"{action} \n {mess}"),
            reply_markup=keyboard,
            parse_mode="HTML"
        )
 