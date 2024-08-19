from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.markdown import hbold

from config import menu
from crud.settings import write_settings, get_settings_user_by_id
from database import Settings
from states.state import SettingsState

settings_router = Router()


@settings_router.message(F.text == "/settings")
async def ask_price(message: types.Message, state: FSMContext):
    """Обработчик для команд settings."""
    get_data_user: Settings | None = await get_settings_user_by_id(
        message.from_user.id
    )

    if get_data_user is None:
        await state.update_data(chat_id=message.from_user.id)
        await state.update_data(update=False)
        await state.set_state(SettingsState.price)
        await message.answer(
            "Введите вашу почасовую ставку: ",
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        kb_list = [[KeyboardButton(text="yes"), KeyboardButton(text="no")]]
        keyword = ReplyKeyboardMarkup(
            keyboard=kb_list,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await state.set_state(SettingsState.change_settings)
        await message.answer(
            text=f"Ваши текущие настройки ⚙️🔧\n"
                 f"---------------------------------------------------------\n"
                 f"Ставка в час: {hbold(get_data_user.price)}₽\n"
                 f"Прибавка за доп час: {hbold(get_data_user.overtime)}₽\n"
                 f"---------------------------------------------------------\n"
                 f"Хотите изменить данные?",
            parse_mode="HTML",
            reply_markup=keyword
        )


@settings_router.message(
    (F.text.lower() == "yes") | (F.text.lower() == "no"),
    SettingsState.change_settings
)
async def change_settings(message: types.Message, state: FSMContext):
    """
    Обрабатывает команды yes and no, при запросе на
    обновление данных о настройках."""
    if message.text == "yes":
        await state.update_data(chat_id=message.from_user.id)
        await state.update_data(update=True)
        await state.set_state(SettingsState.price)
        await message.answer(text="Ok, Введите вашу ставку: ")

    else:
        await state.clear()
        await message.answer(text="Меню", reply_markup=menu)


@settings_router.message(
    F.text.isdigit(),
    SettingsState.price
)
async def ask_chart(message: types.Message, state: FSMContext):
    """Обрабатывает введенную пользователем стоимость часа."""
    await state.update_data(price=int(message.text))
    await state.set_state(SettingsState.overtime_price)

    await message.answer(
        text="Укажите доплату за доп час"
    )


@settings_router.message(
    F.text.isdigit(),
    SettingsState.overtime_price
)
async def ask_price_over_time(
        message: types.Message, state: FSMContext
) -> None:
    """
    Обрабатывает введенную пользователем информацию о вводе
    стоимости о доп часе. И отправляет всю информацию на сохранение в бд.
    """
    await state.update_data(overtime=int(message.text))
    try:
        await write_settings(await state.get_data())

    except ValueError:
        await message.answer(text="Ошибочка вышла((")

    await message.answer(
        text="Отлично, все готово!",
        reply_markup=menu
    )
    await state.clear()
