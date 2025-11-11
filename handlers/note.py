from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from handlers.bot_answer import decorator_errors
from keyboards.note import note_action, back
from states.note import NoteState
from crud.get_data import update_salary
from utils.current_day import gen_message_for_choice_day
from utils.note import answer_after_operation
from loader import notes_empty


note_rout = Router()

@note_rout.callback_query(F.data == "add_note")
@decorator_errors
async def add_note(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Ask the user for a note."""
    data = await state.get_data()
    current_notes: str | None = data.get("current_day", {}).get("notes")
    await state.set_state(NoteState.description)
    
    if current_notes is None:
        current_notes = notes_empty
    else:
        current_notes += f"\n\nДобавте еще запись:"

    await callback.message.edit_text(
        text=hbold(current_notes),
        reply_markup=back,
        parse_mode="HTML"
    )


@note_rout.message(NoteState.description)
@decorator_errors
async def save_description(
    message: Message,
    state: FSMContext
) -> None:
    """Save the note."""
    input_note = message.text
    data = await state.get_data()
    
    current_day: dict = data.get("current_day", {})
    old_notes: str | None = current_day.get("notes")
    if old_notes is None:
        old_notes = 40 * "*"
    day_id = current_day.get("_id")
    
    new_notes = f"{old_notes}\n\n{input_note}\n\n{40 * '*'}"
    current_day.update(notes=new_notes)
    await update_salary(day_id=day_id, data=current_day)
    
    action = "Запись была успешно сохранена.\n"
    await answer_after_operation(message, current_day, action)


@note_rout.callback_query(F.data == "show_note")
@decorator_errors
async def show_notes(
    callback: CallbackQuery, state: FSMContext
) -> None:
    """Show a note for the selected day."""
    data = await state.get_data()
    current_notes: str | None = data.get("current_day", {}).get("notes")
    keyboard = note_action
    
    if current_notes is None:
        current_notes = "Вы еще ничего не написали."
        keyboard = back

    await callback.message.edit_text(
        text=hbold(current_notes),
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@note_rout.callback_query(F.data == "BACK")
@decorator_errors
async def back_by_current_day(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Bring the user back to the selected day."""
    data: dict = await state.get_data()
    current_day: str | None = data.get("current_day", {})
    await answer_after_operation(callback, current_day, "")


@note_rout.callback_query(F.data == "remove_note")
@decorator_errors
async def remove_note(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Delete the note for the selected day."""
    data: dict = await state.get_data()
    current_day: dict = data.get("current_day", {})
    current_day["notes"] = None
    day_id: str = current_day.get("_id")
    await update_salary(day_id=day_id, data=current_day)
    
    action = "Заметки за выбранный день удалены.\n"
    await answer_after_operation(callback, current_day, action)
