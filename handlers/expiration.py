import re
from datetime import date
from typing import List

from asyncpg.pgproto.pgproto import timedelta

from keywords.keyword import cancel_button
from loader import expiration_text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Router
from aiogram import F
from aiogram.utils.markdown import hbold
from states.state import Expiration

expiration = Router()


@expiration.callback_query(F.data == "expiration")
async def input_date(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Expiration.start)
    await callback.message.answer(
        text=expiration_text.format(hbold("дд.мм.гггг"), hbold("- и /")),
        parse_mode="HTML",
        reply_markup=cancel_button,
    )


@expiration.message(Expiration.start)
async def get_expiration_date(message: Message) -> None:
    pattern = r"(\d{2})[./-](\d{2})[./-](\d{4})"
    try:
        expiration_date, days = message.text.split()
        check_date: List[str] = re.findall(pattern, expiration_date)

        if not check_date or not days.isdigit():
            raise ValueError

        input_data: date = date(
            int(check_date[0][2]), int(check_date[0][1]), int(check_date[0][0])
        )

        ended_date: str = (input_data + timedelta(days=int(days))).strftime("%d-%m-%Y")
        await message.answer(
            text=f"Товар хранится до {hbold(ended_date)}."
            f"\n{expiration_text.format(hbold("дд.мм.гггг"), hbold("- и /"))}",
            parse_mode="HTML",
            reply_markup=cancel_button,
        )

    except ValueError:
        await message.answer(
            text=f"Ошибка ввода, попробуйте еще раз.\n"
            f"{expiration_text.format(hbold("дд.мм.гггг"), hbold("- и /"))}",
            parse_mode="HTML",
            reply_markup=cancel_button,
        )
