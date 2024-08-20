import asyncio
import logging

import executor
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import Sequence

from config import BOT_TOKEN
from handlers.month import month_router
from handlers.period import period_router
from handlers.settings import settings_router
from handlers.create import create_router
from handlers.unknown import unknown_rout
from keywords.keyword import mail_menu, menu
from loader import start_text, guide
from states.state import CalcState
from utils.schedule import get_all_users

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(settings_router)
dp.include_router(create_router)
dp.include_router(period_router)
dp.include_router(month_router)
dp.include_router(unknown_rout)


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


@dp.message(CommandStart())
async def handler_start(
        message: types.Message,
        state: FSMContext
) -> None:
    """Обработчик команды старт."""
    await state.clear()
    await message.answer(text=start_text)


@dp.message(F.text == "/contact")
async def community_dev(
        message: types.Message,
        state: FSMContext
) -> None:
    """Обработчик команды связь connection."""
    await state.clear()
    await message.answer(
        text="Связаться с разработчиком",
        reply_markup=mail_menu
    )


@dp.message(F.text == "/main")
async def handle_help(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды help."""
    await state.clear()
    await message.answer("Меню", reply_markup=menu)


@dp.callback_query(F.data == "main")
async def handle_help(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды help."""
    await state.clear()
    await callback.message.delete_reply_markup(inline_message_id=callback.id)
    await callback.message.answer("Меню", reply_markup=menu)


@dp.callback_query(F.data == "calc")
async def calc_input_data(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """Обработчик для команды calc"""
    await state.set_state(CalcState.input)
    await callback.message.answer(
        "Введите что вам нужно посчитать,"
        "например 78 * 12 - 5"
    )


@dp.message(F.text == "/info")
async def guide_information(
        message: types.Message, state: FSMContext
) -> None:
    """Обработчик для команды info"""
    await state.clear()
    await message.answer(text=guide, reply_markup=menu)


@dp.message(CalcState.input)
async def calculate_data(
        message: types.Message,
        state: FSMContext
) -> None:
    """Обработчик для команды clac"""
    try:
        mess = eval(message.text)
        await message.answer(text=str(mess), reply_markup=menu)

    except (SyntaxError, TypeError):
        await state.clear()
        await message.answer(
            text="Введенные данные не отвечают требованиям "
                 "калькулятора. Попробуйте еще раз.",
            reply_markup=menu)


async def send_message_cron():
    users: Sequence = await get_all_users()
    for user in users:
        await bot.send_message(
            user[0].user_chat_id,
            "Добавьте запись об отработанном времени!"
        )


async def main():
    """Запуск бота."""
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    scheduler.add_job(
        send_message_cron,
        'cron',
        hour=19,
        minute=00,
    )
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
