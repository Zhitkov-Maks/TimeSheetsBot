import asyncio
from typing import List
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, \
    InlineKeyboardButton

from config import BOT_TOKEN
from handlers.bot_answer import decorator_errors
from handlers.settings import settings_router
from handlers.month import month_router
from handlers.current_day import create_router
from handlers.add_shifts import shifts_router

from keyboards.keyboard import menu
from loader import start_text, GUIDE, main_text

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(settings_router)
dp.include_router(month_router)
dp.include_router(create_router)
dp.include_router(shifts_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(CommandStart())
@decorator_errors
async def handler_start(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды старт."""
    await state.clear()
    await message.answer(text=start_text, reply_markup=menu)


@dp.message(F.text == "/main")
@decorator_errors
async def handle_help_command(
        message: types.Message,
        state: FSMContext
) -> None:
    """Обработчик команды main."""
    await state.clear()
    await message.answer(main_text, reply_markup=menu)


@dp.message(F.text == "/dev")
@decorator_errors
async def handler_dev(message: types.Message, state: FSMContext) -> None:
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
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=button
    )
    await message.answer("Меню", reply_markup=keyboard)


@dp.callback_query(F.data == "send_email")
@decorator_errors
async def process_email_button(
        callback_query: types.CallbackQuery,
        state: FSMContext
) -> None:
    await state.clear()
    await callback_query.message.answer(
        text="[m-zhitkov@inbox.ru](mailto:m-zhitkov@inbox.ru)",
        parse_mode="Markdown",
        reply_markup=menu
    )


@dp.callback_query(F.data == "main")
@decorator_errors
async def handler_help(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды main."""
    await state.clear()
    await callback.message.edit_text(main_text, reply_markup=menu)


@dp.message(F.text == "/info")
@decorator_errors
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
    try:
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        logger.info("Бот остановлен")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
