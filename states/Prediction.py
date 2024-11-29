from aiogram.fsm.state import StatesGroup, State


class FiveState(StatesGroup):
    weekday: State = State()
    checkbox: State = State()
    how_many_hours = State()
    confirm = State()


class TwoInTwo(StatesGroup):
    weekday: State = State()
    first_day = State()
    how_many_hours = State()
