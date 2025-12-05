from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types

from keyboards.keyboard import back
from loader import unfamiliar_command
from utils.decorate import errors_logger

unknown_rout = Router()


@unknown_rout.message(F.text)
@errors_logger
async def handler_message_unknown(
        message: types.Message, state: FSMContext
) -> None:
    """Show the user that it is impossible to process his command."""
    await state.clear()
    await message.answer(
        text=unfamiliar_command,
        reply_markup=back,
        parse_mode="HTML"
    )


@unknown_rout.callback_query(F.data)
@errors_logger
async def handler_callback_unknown(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Show the user that it is impossible to process his command."""
    await callback.answer(
        text=unfamiliar_command,
        show_alert=True,
    )
