from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from handlers.bot_answer import decorator_errors
from keyboards.keyboard import back, cancel_button
from keyboards.settings import get_actions, settings_choices, SETTINGS
from states.settings import SettingsState
from utils.settings import (
    actions_dict,
    validate_data,
    get_settings_text
)
from crud.settings import create_settings, delete_settings

settings_router: Router = Router()


@settings_router.message(F.text == "/settings")
@decorator_errors
async def choice_options_settings(
    message: Message,
    state: FSMContext
) -> None:
    """Show the user's current settings."""
    await state.clear()
    settings: bool = settings_choices.get(message.from_user.id)
    if settings:
        settings.clear()

    text: str = await get_settings_text(message.from_user.id)
    await message.answer(
        text=hbold(text),
        reply_markup=await get_actions(message.from_user.id),
        parse_mode="HTML"
    )


@settings_router.callback_query(lambda c: c.data.startswith("toggle-"))
@decorator_errors
async def toggle_action(
    callback_query: CallbackQuery,
    state: FSMContext
) -> None:
    """Show me the keyboard in the form of a checkbox."""
    action: str = callback_query.data.split("-")[1]
    user_id: int = callback_query.from_user.id

    if action in settings_choices[user_id]:
        await callback_query.answer(f"Вы убрали: {SETTINGS[action]}")
        settings_choices[user_id].pop(action)

    else:
        settings_choices[user_id].update({action: SETTINGS[action]})
        await callback_query.answer(
            f"Вы выбрали: {SETTINGS[action]}"
        )

    await callback_query.message.edit_reply_markup(
        reply_markup=await get_actions(user_id)
    )


@settings_router.callback_query(F.data == "finish")
@decorator_errors
async def finish_selection(
        call: CallbackQuery, state: FSMContext
) -> None:
    """Add or remove a check mark from the keyboard."""
    options: list[str] = list(settings_choices[call.from_user.id].keys())[::-1]
    await state.update_data(options=options)
    if len(options) == 0:
        await call.answer(
            text="Вы ничего не выбрали",
            reply_markup=back
        )
        return

    action: str = options.pop()
    await state.update_data(action=action)
    await state.set_state(SettingsState.action)
    await call.message.edit_text(
        text=actions_dict[action],
        reply_markup=cancel_button
    )


@settings_router.message(SettingsState.action)
@decorator_errors
async def save_account_name(mess: Message, state: FSMContext) -> None:
    """Ask the user for input while there are still raw fields.."""
    data: dict = await state.get_data()
    options: list = data["options"]
    action: str = data["action"]

    if not await validate_data(action, mess.text):
        await mess.answer(
            hbold("Неверный формат ввода, попробуйте еще раз."),
            reply_markup=cancel_button,
            parse_mode="HTML"
        )
        return

    await state.update_data({action: mess.text})

    if options:
        action = options.pop()
        await state.update_data(action=action)
        await mess.answer(
            text=actions_dict[action],
            reply_markup=cancel_button
        )
        return

    data: dict = await state.get_data()
    del data["action"]
    del data["options"]
    await create_settings(data, mess.from_user.id)
    settings_choices[mess.from_user].clear()
    await mess.answer(
        text="Ваши настройки сохранены.",
        reply_markup=back
    )


@settings_router.callback_query(F.data == "remove_settings")
@decorator_errors
async def remove_user_settings(
        callback: CallbackQuery, state: FSMContext
) -> None:
    """Delete the current settings."""
    await delete_settings(callback.from_user.id)
    await callback.message.edit_text(
        text=hbold("Ваши настройки удалены."),
        reply_markup=back,
        parse_mode="HTML"
    )
