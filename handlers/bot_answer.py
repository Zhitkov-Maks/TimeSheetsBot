from typing import Dict

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from config import BOT_TOKEN
from crud.create import write_salary, update_salary
from loader import success_text
from utils.count import earned_salary
from utils.create_calendar_and_message import create_message

bot = Bot(token=BOT_TOKEN)


async def send_calendar_and_message(
    user: int,
    data: Dict[str, str],
    state: FSMContext
) -> None:
    """
    Отправка пользователю текущего календаря после
    добавления записи за выбранный день.
    """
    message, mess, calendar = await create_message(
        user, data["date"], state
    )

    await bot.send_message(
        chat_id=user,
        text=f"\n\n{message}",
        parse_mode="HTML",
    )

    await bot.send_message(
        chat_id=user,
        text=mess,
        parse_mode="HTML",
        reply_markup=calendar,
    )


async def processing_data(
    user_id: int,
    time: float,
    overtime: float,
    state: FSMContext,
    data: Dict[str, str | int]
) -> None:
    base, overtime, earned = await earned_salary(time, overtime, user_id)
    await bot.send_message(
        chat_id=user_id,
        text=success_text.format(data["date"], hbold(earned)),
        parse_mode="HTML",
    )

    if data["action"] == "add":
        await write_salary(base, overtime, earned, data)

    else:
        await update_salary(base, overtime, earned, data)

    await send_calendar_and_message(user_id, data, state)
