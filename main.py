import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import BOT_TOKEN
from handlers.month import month_router
from handlers.remind import remind
from utils.schedulers import create_scheduler_all
from handlers.settings import settings_router
from handlers.create import create_router
from handlers.unknown import unknown_rout
from handlers.predictions import predict
from keywords.keyword import prediction, menu, cancel_button
from loader import start_text, guide
from states.state import CalcState

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
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
    await message.answer(text=start_text)


@dp.message(F.text == "/prediction")
async def community_dev(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды прогноза"""
    await state.clear()
    await message.answer(
        text="Выберите месяц для прогноза.", reply_markup=await prediction()
    )


@dp.message(F.text == "/main")
async def handle_help(message: types.Message, state: FSMContext) -> None:
    """Обработчик команды help."""
    await state.clear()
    await message.answer("Меню", reply_markup=await menu())


@dp.callback_query(F.data == "main")
async def handle_help(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик команды help."""
    await state.clear()
    await callback.message.delete_reply_markup(inline_message_id=callback.id)
    await callback.message.answer("Меню", reply_markup=await menu())


@dp.callback_query(F.data == "calc")
async def calc_input_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработчик для команды calc"""
    await callback.message.delete_reply_markup(inline_message_id=callback.id)
    await state.set_state(CalcState.input)
    await callback.message.answer(
        "Введите что вам нужно посчитать," "например 78 * 12 - 5",
        reply_markup=cancel_button,
    )


@dp.message(F.text == "/info")
async def guide_information(message: types.Message, state: FSMContext) -> None:
    """Обработчик для команды info"""
    await state.clear()
    await message.answer(text=guide, reply_markup=await menu())


@dp.message(CalcState.input)
async def calculate_data(message: types.Message, state: FSMContext) -> None:
    """Обработчик для команды calc"""
    try:
        mess = eval(message.text)
        await message.answer(text=str(mess), reply_markup=await menu())

    except (SyntaxError, TypeError):
        await state.clear()
        await message.answer(
            text="Введенные данные не отвечают требованиям "
            "калькулятора. Попробуйте еще раз.",
            reply_markup=await menu(),
        )


async def main():
    """Запуск бота."""
    await create_scheduler_all()
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
