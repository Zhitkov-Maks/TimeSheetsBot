from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from sqlalchemy import Sequence

from crud.statistics import get_information_for_month
from keywords.keyword import menu
from utils.genMessagePeriod import generate_str

month_router = Router()


@month_router.callback_query(F.data == "month_current")
async def handle_info_current_month(callback: CallbackQuery):
    """
    Обработчик для команды month_current. Получает информацию
    о текущем месяце.
    """
    result: Sequence = await get_information_for_month(callback.from_user.id)
    month: int = datetime.now().month - 1

    mess_one: str = await generate_str(result, month, period=1)
    await callback.message.answer(mess_one, parse_mode="HTML")

    mess_two: str = await generate_str(result, month, period=2)
    await callback.message.answer(
        mess_two, parse_mode="HTML"
    )

    mess_total: str = await generate_str(result, month, period=0)
    await callback.message.answer(
        mess_total, parse_mode="HTML", reply_markup=await menu()
    )


@month_router.callback_query(F.data == "month_prev")
async def handle_info_prev_month(callback: CallbackQuery):
    """
    Обработчик для команды month_current. Получает информацию о
    прошедшем месяце."""
    result: Sequence = await get_information_for_month(
        callback.from_user.id, 1
    )
    month: int = datetime.now().month - 2

    mess_one: str = await generate_str(result, month, period=1)
    await callback.message.answer(mess_one, parse_mode="HTML")

    mess_two: str = await generate_str(result, month, period=2)
    await callback.message.answer(
        mess_two, parse_mode="HTML"
    )

    mess_total: str = await generate_str(result, month, period=0)
    await callback.message.answer(
        mess_total, parse_mode="HTML", reply_markup=await menu()
    )
