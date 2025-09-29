from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    """
    Класс для определения состояний в процессе работы с текущим днем.
    StatesGroup используется для группировки состояний, связанных с одной задачей.
    """
    check_data: State = State()
    award: State = State()
