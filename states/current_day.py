from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    check_data: State = State()
    other_income: State = State()
