from aiogram.fsm.state import StatesGroup, State


class SalaryState(StatesGroup):
    """
    A class for defining states related to the addition of other income.
    """
    amount: State = State()  # Сумма прочего дохода
    description: State = State()  # Описание
