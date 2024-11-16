from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram import types, F
from aiogram.utils.markdown import hbold

from aiogram_calendar import DialogCalendar

from crud.create import write_salary, update_salary, delete_record
from keywords.keyword import (
    cancel_button,
    confirm_menu,
    menu,
    confirm_menu_two
)
from loader import add_record_text, success_text
from states.state import CreateState
from utils.count import earned_salary

create_router = Router()


@create_router.callback_query(F.data == "select_date")
async def on_date_selected(callback: CallbackQuery) -> None:
    """Обработчик команды select_date. Запускает календарь."""
    await callback.message.answer(
        text="Выберите дату",
        reply_markup=await DialogCalendar().start_calendar()
    )


@create_router.callback_query(F.data.in_(["change", "add"]))
async def on_date_today(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Обработчик команды today, чтобы быстрее
    добавить запись по текущему дню.
    """
    await state.update_data(action=callback.data)
    await state.set_state(CreateState.check_data)
    await callback.message.answer(
        text=add_record_text,
        reply_markup=cancel_button
    )


@create_router.message(CreateState.check_data)
async def check_data(
        message: types.Message,
        state: FSMContext
) -> None:
    numbers: list = message.text.split("*")
    try:
        if len(numbers) == 1 or len(numbers) == 2:

            if len(numbers) == 1:
                time, overtime = float(numbers[0]), 0

            else:
                time, overtime = float(numbers[0]), float(numbers[1])

            await state.set_state(CreateState.select_date)
            await state.update_data(time=time)
            await state.update_data(overtime=overtime)
            await message.answer(
                "Введены корректные данные.",
                reply_markup=confirm_menu
            )
        else:
            raise ValueError

    except ValueError:
        await state.set_state(CreateState.check_data)
        await message.answer(
            "Введенные данные не соответствуют требованиям. \n"
            "Пример: 6.5*5. Попробуйте еще раз.",
            reply_markup=cancel_button
        )


@create_router.callback_query(F.data == "continue", CreateState.select_date)
async def ask_count_hours(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await state.update_data(user_id=callback.from_user.id)
    data: dict = await state.get_data()

    if data.get("action") == "add":
        base, overtime, earned = await earned_salary(
            data["time"], data["overtime"], callback.from_user.id
        )

        await state.update_data(earned=earned)
        await write_salary(base, overtime, earned, data)

        await callback.message.answer(
            text=success_text.format(data["date"], hbold(earned)),
            parse_mode="HTML",
            reply_markup=await menu()
        )

    else:
        if data["time"] == float(0) and data["overtime"] == float(0):
            await state.set_state(CreateState.zero)
            await callback.message.answer(
                text="Вы хотите удалить запись?",
                reply_markup=confirm_menu_two
            )

        else:
            base, overtime, earned = await earned_salary(
                data["time"], data["overtime"], callback.from_user.id
            )

            await state.update_data(earned=earned)
            await update_salary(base, overtime, earned, data)
            await callback.message.answer(
                text=success_text.format(data["date"], hbold(earned)),
                parse_mode="HTML",
                reply_markup=await menu()
            )


@create_router.callback_query(
    (F.data == "cancel") | (F.data == "continue"),
    CreateState.zero
)
async def zero_record(callback: CallbackQuery, state: FSMContext) -> None:
    """Отправка на удаление записи."""
    if callback.data == "cancel":
        await callback.message.answer(
            text="Ок, возвращаю вас в меню.",
            reply_markup=await menu()
        )
    else:
        data = await state.get_data()
        await delete_record(data)
        await callback.message.answer(
            text="Запись была удалена.",
            reply_markup=await menu()
        )
