from aiogram import F, types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from typing import List

from keywords.keyword import menu, cancel_button
from keywords.prediction import prediction, select_schedule_keyboard, \
    get_weekdays_keyboard, user_choices, choices_days, hour_choices
from states.Prediction import TwoInTwo, FiveState
from utils.prediction import get_prediction_sum, two_in_two_get_prediction_sum, \
    get_year_and_month

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
        message: Message, state: FSMContext) -> None:
    await state.update_data(weekdays=int(message.text))
    await state.set_state(FiveState.checkbox)

    await message.answer(
        text="Вы задерживаетесь после 17:00",
        reply_markup=await get_weekdays_keyboard()
    )


@predict.callback_query(lambda c: c.data.startswith("toggle_"))
async def toggle_day(callback_query: types.CallbackQuery):
    day = callback_query.data.split("_")[1]

    # Обновляем состояние выбора
    if not day.isdigit() and day in user_choices:
        user_choices.remove(day)
        await callback_query.answer(f"Вы убрали: {day}")

    elif not day.isdigit() and day not in user_choices:
        user_choices.append(day)
        await callback_query.answer(f"Вы выбрали: {day}")

    elif day.isdigit() and day in hour_choices:
        hour_choices.remove(day)
        await callback_query.answer(f"Вы убрали: {day}")

    elif day.isdigit() and day not in hour_choices:
        hour_choices.append(day)
        await callback_query.answer(f"Вы выбрали: {day}")

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_weekdays_keyboard())


@predict.callback_query(F.data == "finish")
async def finish_selection(
        callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    delay_list: List[int] = []
    if user_choices:
        await callback_query.answer(
            f"Ваши выбранные дни: {', '.join(user_choices)}")
        for i in user_choices:
            delay_list.append(choices_days.get(i))
        await state.update_data(delay=delay_list)

    else:
        await state.update_data(delay="delay_no")

    if hour_choices:
        await state.update_data(hour=hour_choices[0])
    else:
        await state.update_data(hour=3)

    data: dict = await state.get_data()
    prediction_sum: int = await get_prediction_sum(callback_query.from_user.id, data)
    await callback_query.message.answer(
        text=f"Ваш прогнозируемый заработок составит {prediction_sum:,.2f}₽",
        reply_markup=await menu()
    )
    user_choices.clear()
    hour_choices.clear()
