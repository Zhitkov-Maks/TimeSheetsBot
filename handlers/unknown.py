from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types

from handlers.bot_answer import decorator_errors
from keywords.keyword import menu
from loader import unfamiliar_command

unknown_rout = Router()


@unknown_rout.message(F.text)
@decorator_errors
async def handler_message_unknown(
        message: types.Message, state: FSMContext
) -> None:
    """Обрабатывает неизвестные команды."""
    await state.clear()
    await message.answer(text=unfamiliar_command, reply_markup=menu)
