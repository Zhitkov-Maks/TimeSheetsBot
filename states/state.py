from aiogram.fsm.state import StatesGroup, State


class MonthState(StatesGroup):
    choice: State = State()


class SettingsState(StatesGroup):
    price: State = State()
    change_settings: State = State()
    overtime_price: State = State()


class CreateState(StatesGroup):
    check_data: State = State()
    other_income: State = State()


class PeriodState(StatesGroup):
    month: State = State()
    year: State = State()

class RemindState(StatesGroup):
    """Класс состояний для напоминаний."""

    start: State = State()
    add: State = State()
    confirm: State = State()


class Expiration(StatesGroup):
    start: State = State()
    end: State = State()


class StatisticState(StatesGroup):
    year: State = State()
