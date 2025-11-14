import asyncio
from typing import List

from aiogram import Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold

from config import bot
from handlers.bot_answer import decorator_errors
from handlers.settings import settings_router
from handlers.month import month_router
from handlers.current_day import day_router
from handlers.add_shifts import shifts_router
from handlers.salary import salary
from handlers.unknown import unknown_rout
from handlers.statistic import statistick_router
from handlers.note import note_rout
from handlers.valute import money

from loader import start_text, GUIDE, main_text


dp = Dispatcher(bot=bot)
dp.include_router(settings_router)
dp.include_router(month_router)
dp.include_router(day_router)
dp.include_router(shifts_router)
dp.include_router(salary)
dp.include_router(money)
dp.include_router(statistick_router)
dp.include_router(note_rout)
dp.include_router(unknown_rout)


@dp.message(CommandStart())
@decorator_errors
async def handler_start(message: types.Message, state: FSMContext) -> None:
    """The handler for the start command."""
    await state.clear()
    await message.answer(text=start_text, parse_mode="HTML")


@dp.message(F.text == "/dev")
@decorator_errors
async def handler_dev(message: types.Message, state: FSMContext) -> None:
    """The handler for the dev command."""
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
    """Show the user the email."""
    await state.clear()
    await callback_query.message.answer(
        text="[m-zhitkov@inbox.ru](mailto:m-zhitkov@inbox.ru)",
    )


@dp.message(F.text == "/info")
@decorator_errors
async def guide_information(message: types.Message, state: FSMContext) -> None:
    """The handler for the info command."""
    await state.clear()
    await message.answer(text=GUIDE, parse_mode="HTML")
    await message.answer(
        text="Меню.\n/main - чтобы открыть меню."
    )


async def main():
    """Launch the bot."""
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
