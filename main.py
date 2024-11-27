import asyncio
import logging
from logging import DEBUG

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import BOT_TOKEN
from handlers.create import create_router
from handlers.expiration import expiration
from handlers.month import month_router
from handlers.predictions import predict
from handlers.remind import remind
from handlers.settings import settings_router
from handlers.statistics import statistic
from handlers.unknown import unknown_rout
from keywords.keyword import menu
from loader import start_text, guide
from utils.schedulers import create_scheduler_all

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(statistic)
dp.include_router(expiration)
dp.include_router(settings_router)
dp.include_router(create_router)
dp.include_router(month_router)
dp.include_router(predict)
dp.include_router(remind)
dp.include_router(unknown_rout)


@dp.message(CommandStart())
async def handler_start(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды старт."""
    await state.clear()
    await message.delete()
    await message.answer(
        text=start_text,
        reply_markup=await menu()
    )

@dp.message(F.text == "/main")
async def handle_help_command(message: types.Message,
                              state: FSMContext) -> None:
    """Обработчик команды main."""
    await state.clear()
    await message.answer("Меню", reply_markup=await menu())


@dp.callback_query(F.data == "main")
async def handle_help(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды main."""
    await state.clear()
    await callback.message.answer("Меню", reply_markup=await menu())


@dp.message(F.text == "/info")
async def guide_information(message: types.Message, state: FSMContext) -> None:
    """Обработчик для команды info"""
    await message.answer(text=guide, reply_markup=await menu())
    await state.clear()


async def main():
    """Запуск бота."""
    await create_scheduler_all()
    logging.basicConfig(level=DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
