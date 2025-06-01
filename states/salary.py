from aiogram.fsm.state import StatesGroup, State


class SalaryState(StatesGroup):
    """
    Класс для определения состояний, связанный с добавлением прочего дохода.
    """
    amount: State = State()  # Сумма прочего дохода
    description: State = State()  # Описание
