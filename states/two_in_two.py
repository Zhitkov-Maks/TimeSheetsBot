from aiogram.fsm.state import StatesGroup, State


class TwoInTwo(StatesGroup):
    """
    Класс для определения состояний при прогнозировании з/п для графика
    два через два.
    """
    count_weekday: State = State()  # Состояние для выбора количества дней для подработок.
    first_day: State = State()  # Состояние для указания первого дня.
    how_many_hours: State = State()  # Состояние для ввода количества часов.
