from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    price = State()
    change_settings = State()
    overtime_price = State()


class CreateState(StatesGroup):
    select_date = State()
    confirm = State()


class PeriodState(StatesGroup):
    month = State()
    year = State()


class CalcState(StatesGroup):
    input = State()
