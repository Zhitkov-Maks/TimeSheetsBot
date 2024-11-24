import asyncio

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from crud.settings import write_settings, get_settings_user_by_id
from database import Settings
from handlers.bot_answer import delete_message_after_delay
from keywords.keyword import menu, confirm_menu, cancel_button
from states.state import SettingsState

settings_router = Router()


@settings_router.callback_query(F.data == "settings")
async def ask_price(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик для команд settings."""
    await callback.message.delete_reply_markup(inline_message_id=callback.id)
    get_data_user: Settings | None = await get_settings_user_by_id(
        callback.from_user.id
    )

    if get_data_user is None:
        await state.update_data(chat_id=callback.from_user.id)
        await state.update_data(update=False)
        await state.set_state(SettingsState.price)
        send_message: Message = await callback.message.answer(
            "Введите вашу почасовую ставку: ",
            reply_markup=cancel_button,
        )

    else:
        await state.set_state(SettingsState.change_settings)
        send_message: Message = await callback.message.answer(
            text=f"Ваши текущие настройки ⚙️🔧\n"
            f"---------------------------------------------------------\n"
            f"Ставка в час: {hbold(get_data_user.price)}₽\n"
            f"Прибавка за доп час: {hbold(get_data_user.overtime)}₽\n"
            f"---------------------------------------------------------\n"
            f"Хотите изменить данные?",
            parse_mode="HTML",
            reply_markup=confirm_menu,
        )
    await asyncio.create_task(delete_message_after_delay(callback.message, 0))
    await asyncio.create_task(delete_message_after_delay(send_message, 60))


@settings_router.callback_query(F.data == "continue", SettingsState.change_settings)
async def change_settings(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает команды yes and no, при запросе на
    обновление данных о настройках."""
    await state.update_data(chat_id=callback.from_user.id)
    await state.update_data(update=True)
    await state.set_state(SettingsState.price)

    send_message: Message = await callback.message.answer(text="Ok, Введите вашу ставку: ")
    await asyncio.create_task(delete_message_after_delay(send_message, 60))


@settings_router.message(F.text.isdigit(), SettingsState.price)
async def ask_chart(message: types.Message, state: FSMContext):
    """Обрабатывает введенную пользователем стоимость часа."""
    await state.update_data(price=int(message.text))
    await state.set_state(SettingsState.overtime_price)

    send_message: Message = await message.answer(text="Укажите доплату за доп час")

    await asyncio.create_task(delete_message_after_delay(message, 60))
    await asyncio.create_task(delete_message_after_delay(send_message, 0))


@settings_router.message(F.text.isdigit(), SettingsState.overtime_price)
async def ask_price_over_time(message: types.Message, state: FSMContext) -> None:
    """
    Обрабатывает введенную пользователем информацию о вводе
    стоимости о доп часе. И отправляет всю информацию на сохранение в бд.
    """
    await state.update_data(overtime=int(message.text))
    try:
        await write_settings(await state.get_data())
        send_message: Message = await message.answer(text="Отлично, все готово!",
                             reply_markup=await menu())

    except ValueError:
        send_message: Message = await message.answer(text="Ошибочка вышла((")

    await state.clear()
    await asyncio.create_task(delete_message_after_delay(message, 60))
    await asyncio.create_task(delete_message_after_delay(send_message, 0))
