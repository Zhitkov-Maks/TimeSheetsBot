from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    """
    A class for defining states in the process of working 
    with the current day.
    """
    check_data: State = State()
    award: State = State()
