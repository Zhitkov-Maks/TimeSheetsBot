from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from config import BOT_TOKEN
from handlers.bot_answer import decorator_errors
from keyboards.keyboard import back
from utils.salary import get_message_by_expected_salary

salary: Router = Router()
bot = Bot(token=BOT_TOKEN)


@salary.callback_query(F.data == "expected_salary")
@decorator_errors
async def get_expected_salary(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """
    Обработчик команды получения ожидаемых
    денежных поступлений в текущем месяце.
    """
    message: str = await get_message_by_expected_salary(callback.from_user.id)
    await callback.message.edit_text(
        text=hbold(message),
        reply_markup=back,
        parse_mode="HTML"
    )
