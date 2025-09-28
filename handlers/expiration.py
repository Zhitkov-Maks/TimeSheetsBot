import re
from datetime import datetime, timedelta as td
from dateutil.relativedelta import relativedelta

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.keyboard import cancel_button
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import State, StatesGroup

from utils.common import is_valid_date


date_router = Router()

date_pattern = re.compile(
    r'^\d{2}([-/\.])\d{2}\1\d{4}$'
)


class StateDate(StatesGroup):
    date = State()
    term = State()


@date_router.callback_query(F.data == "expiration_date")
async def expiration_date_start(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Спроси дату изготовления."""
    await state.set_state(StateDate.date)
    await callback.message.answer(
        text=hbold("Введите дату изготовления в виде(01(-,./)01(-,/)2025): "),
        reply_markup=cancel_button,
        parse_mode="HTML"
    )


@date_router.message(StateDate.date)
async def get_date_pruduced(
    message: Message,
    state: FSMContext
) -> None:
    """
    Проверь введенную дату и если дата корректно спроси срок хранения.
    """
    if date_pattern.match(message.text) and is_valid_date(message.text):
        date_ = message.text
        format_str = f"{date_[:2]}-{date_[3:5]}-{date_[6:]}"
        await state.set_state(StateDate.term)
        await state.update_data(date=format_str)
        await message.answer(
            text=hbold(
                "Введние через пробел данные:\n"
                "d 100 - если срок годности в днях;\n"
                "m 6 - если срок годности в месяцах;\n"
                "y 2 - если в годах."
            ),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text=hbold("Неверный ввод, попробуйте еще раз."),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )


@date_router.message(StateDate.term)
async def get_term(
    message: Message,
    state: FSMContext
) -> None:
    letters = ("d", "D", "m", "M", "y", "Y", "д", "Д", "м", "М", "г", "Г")
    term: list = message.text.split()
    if (
        len(term) != 2
        or term[0] not in letters
        or not term[1].isdigit()
    ):
        await message.answer(
            text=hbold("Ошибка ввода попробуйте еще раз."),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )
    else:
        input_date = (await state.get_data()).get("date")
        input_date = datetime.strptime(input_date, "%d-%m-%Y")

        if term[0].lower() == "d" or term[0].lower() == "д":
            end_date = str(input_date + td(days=int(term[1])))
        elif term[0].lower() == "m" or term[0].lower() == "м":
            end_date = str(input_date + relativedelta(months=int(term[1])))
        else:
            end_date = str(input_date + relativedelta(years=int(term[1])))

        await state.set_state(StateDate.date)
        str_date = f"{end_date[8:10]}.{end_date[5:7]}.{end_date[:4]}"
        await message.answer(
            text=hbold(
                f"Дата окончания срока: {str_date}.\n"
                f"Введите дату изготовления товара: "
            ),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )
