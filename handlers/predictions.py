from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keywords.prediction import prediction, select_schedule_keyboard
from utils.prediction import get_year_and_month

predict: Router = Router()


@predict.callback_query(F.data == "prediction")
async def start_prediction(callback: CallbackQuery) -> None:
    """
    Обработчик команды прогноза. Показывает инлайн
    клавиатуру для выбора месяца.
    """
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text="Выберите месяц для прогноза.", reply_markup=await prediction()
    )


@predict.callback_query(F.data.in_(["current", "next_month"]))
async def get_prediction_month(callback: CallbackQuery, state: FSMContext):
    """Обработчик ответа выбора месяца. Добавляет выбранный месяц и
    год в словарь, и показывает инлайн клавиатуру для выбора графика.
    """
    year, month = await get_year_and_month(callback.data)
    await state.update_data(year=year, month=month)
    await callback.message.answer(
        text="Выберите график: ",
        reply_markup=select_schedule_keyboard
    )
