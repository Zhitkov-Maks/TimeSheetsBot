from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types

from config import menu

unknown_rout = Router()


@unknown_rout.message(F.text)
async def handler_message_unknown(
        message: types.Message, state: FSMContext
):
    """Обрабатывает неизвестные команды."""
    await state.clear()
    await message.answer(
        "Введенная команда мне не знакома, будьте внимательнее.",
        reply_markup=menu
    )
