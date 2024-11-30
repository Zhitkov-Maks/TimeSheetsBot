from aiogram.fsm.state import StatesGroup, State


class ShiftsState(StatesGroup):
    """
    Класс для определения состояний в процессе работы со сменами.
    StatesGroup используется для группировки состояний, связанных с одной задачей.
    """
    month: State = State()  # Состояние для выбора месяца
    hours: State = State()  # Состояние для ввода количества часов
