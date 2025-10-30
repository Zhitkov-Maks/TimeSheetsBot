from aiogram.fsm.state import StatesGroup, State


class NoteState(StatesGroup):
    """
    Класс для определения состояний, связанный с добавлением заметок.
    """
    description: State = State()
