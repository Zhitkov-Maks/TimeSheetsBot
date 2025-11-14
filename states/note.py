from aiogram.fsm.state import StatesGroup, State


class NoteState(StatesGroup):
    """A class for defining states related to adding notes."""
    description: State = State()
