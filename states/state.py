from aiogram.fsm.state import StatesGroup, State


class MonthState(StatesGroup):
    choice = State()


class SettingsState(StatesGroup):
    price = State()
    change_settings = State()
    overtime_price = State()


class CreateState(StatesGroup):
    check_data = State()
    select_date = State()
    confirm = State()
    zero = State()


class PeriodState(StatesGroup):
    month = State()
    year = State()


class CalcState(StatesGroup):
    input = State()
