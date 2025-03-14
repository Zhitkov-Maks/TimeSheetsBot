from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    """
    Класс для определения состояний, связанных с настройками стоимости работы.
    Используется для управления состояниями, связанными с изменением настроек.
    """
    action: State = State()
