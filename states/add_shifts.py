from aiogram.fsm.state import StatesGroup, State


class ShiftsState(StatesGroup):
    """A class for working on adding shifts in groups."""
    month: State = State()  # Состояние для выбора месяца
    hours: State = State()  # Состояние для ввода количества часов
