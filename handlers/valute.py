from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from keyboards.keyboard import menu
from utils.valute import get_valute_info


money = Router()


@money.callback_query(F.data == "valute")
async def valute_info(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Покажи пользователю курс рубля."""
    message = await get_valute_info()
    await callback.message.answer(
        text=hbold(message),
        reply_markup=menu,
        parse_mode="HTML"
    )
