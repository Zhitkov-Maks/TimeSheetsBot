from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.bot_answer import decorator_errors
from keywords.prediction import select_schedule_keyboard, prediction_button
from loader import MONTH_DATA
from states.prediction import Prediction
from utils.prediction import get_year_and_month

predict: Router = Router()


@predict.callback_query(F.data == "prediction")
@decorator_errors
async def start_prediction(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик команды прогноза. Показывает инлайн
    клавиатуру для выбора месяца.
    """
    await callback.message.delete_reply_markup()
    await state.set_state(Prediction.month)
    await callback.message.answer(
        text="Выберите месяц для прогноза.",
        reply_markup=await prediction_button()
    )


@predict.callback_query(Prediction.month, F.data.in_(["current", "next_month"]))
@decorator_errors
async def get_prediction_month(
        callback: CallbackQuery,
        state: FSMContext
) -> None:
    """Обработчик ответа выбора месяца. Добавляет выбранный месяц и
    год в словарь, и показывает инлайн клавиатуру для выбора графика.
    """
    year, month = await get_year_and_month(callback.data)
    await callback.message.delete_reply_markup()
    await state.update_data(year=year, month=month)
    await callback.message.answer(
        text=f"Вы выбрали ( {MONTH_DATA[month]} ). Выберите график 🛠🔧 работы: ",
        reply_markup=select_schedule_keyboard
    )
