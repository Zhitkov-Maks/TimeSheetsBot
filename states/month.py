from aiogram.fsm.state import StatesGroup, State


class MonthState(StatesGroup):
    """
    A class for determining the conditions associated 
    with the choice of the month.
    It is used to manage the status of the user's month selection.
    """
    choice: State = State()  # Состояние для выбора месяца
