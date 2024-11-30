from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    """
    Класс для определения состояний, связанных с настройками стоимости работы.
    Используется для управления состояниями, связанными с изменением настроек.
    """
    price: State = State()  # Состояние для ввода цены
    change_settings: State = State()  # Состояние для изменения других настроек
    overtime_price: State = State()  # Состояние для ввода цены за сверхурочные
    # часы
