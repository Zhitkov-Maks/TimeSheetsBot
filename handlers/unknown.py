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
        "Не могу обработать введенную команду.\n"
        "Возможные причины: \n"
        "- Необходимо было ввести число, а введена была"
        " строка.\n"
        "- Вместо выбора да или нет вы ввели что-то свое.\n"
        "Попробуйте сначала, и будьте внимательны.",
        reply_markup=menu
    )
