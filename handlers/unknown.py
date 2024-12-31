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
    """
    Обрабатывает либо неизвестные команды, либо неправильный ввод,
    когда например, нужно ввести число, а пользователь вводит строку, то
    пользователь попадет сюда.
    """
    await state.clear()
    await message.answer(text=unfamiliar_command, reply_markup=menu)


@unknown_rout.callback_query(F.data)
@decorator_errors
async def handler_callback_unknown(
        callback: types.CallbackQuery, state: FSMContext
) -> None:
    """
    Обрабатывает кнопки, которые не содержат на себе никаких данных.
    """
    await callback.answer(
        text="На меня не нужно нажимать, на мне нет никакой информации. "
             "Надеюсь на понимание.", show_alert=True
    )
