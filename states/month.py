from aiogram.fsm.state import StatesGroup, State


class MonthState(StatesGroup):
    """
    Класс для определения состояний, связанных с выбором месяца.
    Используется для управления состоянием выбора месяца пользователем.
    """
    choice: State = State()  # Состояние для выбора месяца
