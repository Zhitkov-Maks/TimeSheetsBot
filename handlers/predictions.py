from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keywords.keyword import menu, cancel_button
from keywords.prediction import prediction, select_schedule_keyboard, \
    delay_keyboard
from states.Prediction import TwoInTwo, FiveState
from utils.prediction import get_prediction_sum, get_year_and_month, \
    two_in_two_get_prediction_sum

predict = Router()


@predict.callback_query(F.data == "prediction")
async def start_prediction(callback: CallbackQuery) -> None:
    """Обработчик команды прогноза"""
    await callback.message.answer(
        text="Выберите месяц для прогноза.", reply_markup=await prediction()
    )


@predict.callback_query(F.data.in_(["current", "next_month"]))
async def get_prediction_month(callback: CallbackQuery, state: FSMContext):
    """."""
    year, month = await get_year_and_month(callback.data)
    await state.update_data(year=year, month=month)
    await callback.message.answer(
        text="Выберите график: ",
        reply_markup=select_schedule_keyboard
    )


@predict.callback_query(F.data == "two_in_two")
async def two_in_to_get_prediction_scheduler(callback: CallbackQuery,
                                             state: FSMContext):
    await state.set_state(TwoInTwo.weekday)
    await callback.message.answer(
        text="Сколько дополнительных смен вы хотите отработать.",
        reply_markup=cancel_button
    )


@predict.message(TwoInTwo.weekday, F.text.isdigit())
async def two_in_to_get_prediction_first_day(
        message: Message,
        state: FSMContext
) -> None:
    await state.update_data(weekdays=int(message.text))
    await state.set_state(TwoInTwo.first_day)

    await message.answer(
        text="Какого числа ваш первый рабочий день в выбранном месяце?",
        reply_markup=cancel_button
    )


@predict.message(TwoInTwo.first_day, F.text.isdigit())
async def two_in_to_get_prediction_final(
        message: Message,
        state: FSMContext
) -> None:
    await state.update_data(first_day=int(message.text))
    data = await state.get_data()
    prediction_sum = await two_in_two_get_prediction_sum(message.from_user.id,
                                                         data)
    await message.answer(
        text=f"Ваш прогнозируемый заработок составит {prediction_sum:,.2f}₽",
        reply_markup=await menu()
    )


@predict.callback_query(F.data == "five_days")
async def five_days_get_prediction_scheduler(callback: CallbackQuery,
                                             state: FSMContext):
    await state.set_state(FiveState.weekday)
    await callback.message.answer(
        text="Сколько дополнительных смен вы хотите отработать.",
        reply_markup=cancel_button
    )


@predict.message(FiveState.weekday, F.text.isdigit())
async def five_days_get_prediction_delay(
        message: Message,
        state: FSMContext
) -> None:
    await state.update_data(weekdays=int(message.text))
    await state.set_state(FiveState.confirm)

    await message.answer(
        text="Вы задерживаетесь после 17:00",
        reply_markup=delay_keyboard
    )


@predict.callback_query(FiveState.confirm)
async def five_days_get_prediction_final(
        callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(delay=callback.data)
    data: dict = await state.get_data()
    prediction_sum: int = await get_prediction_sum(callback.from_user.id, data)
    await callback.message.answer(
        text=f"Ваш прогнозируемый заработок составит {prediction_sum:,.2f}₽",
        reply_markup=await menu()
    )
