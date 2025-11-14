from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    """A class for working with user settings."""
    action: State = State()
