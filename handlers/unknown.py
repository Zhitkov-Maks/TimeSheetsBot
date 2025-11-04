from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types

from handlers.bot_answer import decorator_errors
from keyboards.keyboard import menu
from loader import unfamiliar_command

unknown_rout = Router()


@unknown_rout.message(F.text)
@decorator_errors
async def handler_message_unknown(
        message: types.Message, state: FSMContext
) -> None:
    """Show the user that it is impossible to process his command."""
    await state.clear()
    await message.answer(text=unfamiliar_command, reply_markup=menu)


@unknown_rout.callback_query(F.data)
@decorator_errors
async def handler_callback_unknown(
        callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Show the user that it is impossible to process his command."""
    await callback.answer(text=unfamiliar_command, show_alert=True)
