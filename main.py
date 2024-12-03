import asyncio
import logging
from logging import DEBUG
from typing import List

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton

from config import BOT_TOKEN
from handlers.add_shifts import shifts_router
from handlers.current_day import create_router
from handlers.five_days import five_days_router
from handlers.month import month_router
from handlers.predictions import predict
from handlers.settings import settings_router
from handlers.statistics import statistic
from handlers.two_in_two import two_in_two_router
from handlers.unknown import unknown_rout
from keywords.keyword import menu
from loader import start_text, GUIDE
from utils.five_days import clear_data

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(statistic)
dp.include_router(settings_router)
dp.include_router(create_router)
dp.include_router(month_router)
dp.include_router(predict)
dp.include_router(two_in_two_router)
dp.include_router(five_days_router)
dp.include_router(shifts_router)
dp.include_router(unknown_rout)


@dp.message(CommandStart())
async def handler_start(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды старт."""
    await state.clear()
    await message.answer(text=start_text, reply_markup=menu)


@dp.message(F.text == "/main")
async def handle_help_command(
        message: types.Message,
        state: FSMContext
) -> None:
    """Обработчик команды main."""
    await state.clear()
    await message.answer("Меню", reply_markup=menu)


@dp.message(F.text == "/dev")
async def handle_help_command(
        message: types.Message,
        state: FSMContext
) -> None:
    """Обработчик команды main."""
    await state.clear()
    button: List[List[InlineKeyboardButton]] = [
            [
                InlineKeyboardButton(
                    text="Мой Email", callback_data="send_email"),
                InlineKeyboardButton(
                    text="Мой Телеграм", url="https://t.me/Maksim1Zhitkov"),
            ]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer("Меню", reply_markup=keyboard)


@dp.callback_query(F.data == "send_email")
async def process_email_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        text="[m-zhitkov@inbox.ru](mailto:m-zhitkov@inbox.ru)",
        parse_mode="Markdown",
        reply_markup=menu
    )


@dp.callback_query(F.data == "main")
async def handler_help(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды main."""
    await callback.message.delete_reply_markup()
    await state.clear()
    await clear_data()
    await callback.message.answer("Меню", reply_markup=menu)


@dp.message(F.text == "/info")
async def guide_information(message: types.Message, state: FSMContext) -> None:
    """Обработчик для команды info"""
    await state.clear()
    for mess in GUIDE:
        await message.answer(text=mess)
    await message.answer(
        text="Меню",
        reply_markup=menu
    )


async def main():
    """Запуск бота."""
    logging.basicConfig(level=DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
