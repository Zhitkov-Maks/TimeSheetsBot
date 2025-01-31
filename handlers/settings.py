from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from crud.settings import write_settings, get_settings_user_by_id
from database import Settings
from handlers.bot_answer import decorator_errors
from keywords.keyword import menu, confirm_menu, cancel_button
from states.settings import SettingsState

settings_router: Router = Router()

@settings_router.callback_query(F.data == "settings")
@decorator_errors
async def ask_price(callback: CallbackQuery, state: FSMContext):
    """Обработчик для команд settings. Если у пользователя еще нет настроек,
    то просит пользователя сразу ввести нужные данные, иначе спрашивает,
    хочет ли пользователь изменить настройки.
    """
    await callback.message.delete_reply_markup()
    get_data_user: Settings | None = await get_settings_user_by_id(
        callback.from_user.id
    )

    if get_data_user is None:
        await state.update_data(chat_id=callback.from_user.id)
        await state.update_data(update=False)
        await state.set_state(SettingsState.price)
        await callback.message.answer(
            "Введите вашу почасовую ставку: ",
            reply_markup=cancel_button,
        )

    else:
        await state.set_state(SettingsState.change_settings)
        await callback.message.answer(
            text=f"Ваши текущие настройки ⚙️🔧\n\n"
                 f"Ставка в час: {hbold(get_data_user.price)}₽\n"
                 f"Доплата: {hbold(get_data_user.overtime)}₽\n\n"
                 f"Хотите изменить данные?",
            parse_mode="HTML",
            reply_markup=confirm_menu,
        )


@settings_router.callback_query(
    F.data == "continue", SettingsState.change_settings)
@decorator_errors
async def change_settings(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает команды yes and no, при запросе на
    обновление данных о настройках."""
    await callback.message.delete_reply_markup()
    await state.update_data(chat_id=callback.from_user.id)
    await state.update_data(update=True)
    await state.set_state(SettingsState.price)

    await callback.message.answer(text="Ok, Введите вашу ставку: ")


@settings_router.message(F.text.isdigit(), SettingsState.price)
@decorator_errors
async def ask_chart(message: Message, state: FSMContext):
    """Обрабатывает введенную пользователем стоимость часа."""
    await state.update_data(price=int(message.text))
    await state.set_state(SettingsState.overtime_price)

    await message.answer(
        text="Укажите доплату за переработку, если доплаты нет введите 0.")


@settings_router.message(F.text.isdigit(), SettingsState.overtime_price)
@decorator_errors
async def ask_price_over_time(
        message: Message,
        state: FSMContext
) -> None:
    """
    Обрабатывает введенную пользователем информацию о вводе
    стоимости о доп часе. И отправляет всю информацию на сохранение в бд.
    """
    await state.update_data(overtime=int(message.text))
    try:
        await write_settings(await state.get_data())
        await message.answer(
            text="Отлично, все готово!",
            reply_markup=menu)

    except ValueError:
        await message.answer(text="Ошибочка вышла((")

    await state.clear()
