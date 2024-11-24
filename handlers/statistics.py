import asyncio
from datetime import datetime
from typing import List

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, \
    InlineKeyboardMarkup, Message
from sqlalchemy import Row

from config import BOT_TOKEN
from crud.statistics import request_statistic
from handlers.bot_answer import delete_message_after_delay
from keywords.keyword import menu
from states.state import StatisticState
from utils.gen_statistic_message import gen_message_statistic

statistic: Router = Router()
bot = Bot(token=BOT_TOKEN)


@statistic.callback_query(F.data == "statistic")
async def get_statistics(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды получения статистики. Показывает клавиатуру для
    выбора года.
    """
    year: int = datetime.now().year
    keyword: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text=f"{year} г", callback_data=str(year)),
            InlineKeyboardButton(text=f"{year - 1} г", callback_data=str(year - 1)),
            InlineKeyboardButton(text=f"{year - 2} г.", callback_data=str(year - 2)),
        ],
        [InlineKeyboardButton(text="Показать меню", callback_data="main")],
    ]
    await state.set_state(StatisticState.year)
    await callback.message.answer(
        text="Выберите год.", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyword)
    )
    await asyncio.create_task(delete_message_after_delay(callback.message, 0))


@statistic.callback_query(StatisticState.year)
async def choice_year(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Показа статистики за выбранный год.
    """
    year: int = int(callback.data)
    result: Row[tuple] = await request_statistic(callback.from_user.id, year)
    await state.clear()
    if result[0] is not None:
        mess: str = await gen_message_statistic(result, year)

        sent_message: Message = await callback.message.answer(
            text=mess, parse_mode="HTML", reply_markup=await menu()
        )

        await asyncio.create_task(
            delete_message_after_delay(callback.message, 0))
        await asyncio.create_task(
            delete_message_after_delay(sent_message, 60))

    else:
        await callback.message.answer(
            text="За выбранный год нет данных.", reply_markup=await menu()
        )
