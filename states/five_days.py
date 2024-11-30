from aiogram.fsm.state import StatesGroup, State


class FiveState(StatesGroup):
    """
    Класс для определения состояний при прогнозировании з/п для
    пятидневной рабочей недели.
    """
    weekday: State = State()  # Состояние для выбора дня недели
    checkbox: State = State()  # Состояние для обработки чекбоксов
        # (например, выбор дней)
    how_many_hours: State = State()  # Состояние для ввода количества часов
    confirm: State = State()  # Состояние для подтверждения выбора
