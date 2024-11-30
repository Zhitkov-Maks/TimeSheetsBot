from aiogram.fsm.state import StatesGroup, State


class StatisticState(StatesGroup):
    """
    Класс для определения состояний, связанных со статистикой.
    Используется для управления состоянием выбора года для получения
    статистических данных.
    """
    year: State = State()  # Состояние для выбора года
