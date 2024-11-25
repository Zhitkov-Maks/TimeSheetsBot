from aiogram.fsm.state import StatesGroup, State


class FiveState(StatesGroup):
    weekday: State = State()
    confirm = State()


class TwoInTwo(StatesGroup):
    weekday: State = State()
    first_day = State()
