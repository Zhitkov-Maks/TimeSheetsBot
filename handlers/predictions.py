from datetime import datetime as dt

from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import F
from keywords.keyword import menu
from utils.prediction import get_prediction_sum

predict = Router()


@predict.callback_query(F.data == "current_prediction")
async def handle_info_current_month(callback: CallbackQuery):
    """
    Обработчик для команды month_current. Возвращает примерную за
    текущем месяц.
    """
    month: int = dt.now().month
    year: int = dt.now().year
    prediction_sum: int = await get_prediction_sum(month, year, callback.from_user.id)
    await callback.message.answer(
        text=f"Прогнозируемый заработок {prediction_sum}.", reply_markup=await menu()
    )


@predict.callback_query(F.data == "next_prediction")
async def handle_info_current_month_next(callback: CallbackQuery):
    """
    Обработчик для команды month_current. Возвращает примерную за
    следующий месяц.
    """
    month: int = (dt.now().month + 1) % 12

    if month == 0:
        month = 12

    year: int = dt.now().year

    if dt.now().month == 12:
        year += 1

    prediction_sum: int = await get_prediction_sum(month, year, callback.from_user.id)

    await callback.message.answer(
        text=f"Прогнозируемый заработок {prediction_sum}.", reply_markup=await menu()
    )
