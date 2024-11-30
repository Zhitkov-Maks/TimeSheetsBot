from aiogram.fsm.state import StatesGroup, State


class Prediction(StatesGroup):
    """
    Класс для определения состояний, связанных с прогнозированием з/п.
    Используется для управления состоянием выбора месяца для прогнозирования.
    """
    month: State = State()  # Состояние для выбора месяца
