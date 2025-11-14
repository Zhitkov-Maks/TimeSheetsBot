from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from keyboards.keyboard import back
from utils.decorate import errors_logger
from utils.valute import get_valute_show_message


money = Router()


@money.message(F.text == "/currency")
@errors_logger
async def valute_info(
    message: Message,
    state: FSMContext
) -> None:
    """Show the user the ruble exchange rate."""
    mess = await get_valute_show_message()
    await message.answer(
        text=hbold(mess),
        reply_markup=back,
        parse_mode="HTML"
    )
