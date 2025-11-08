import re

from crud.settings import get_settings_user_by_id
from keyboards.settings import SETTINGS
from database.db_conf import MongoDB
from loader import money

number_pattern = r'^-?\d+(\.\d+)?$'

actions_dict: dict[str, str] = {
    "price_time": "Введите вышу почасовую оплату труда.",
    "price_overtime": "Ввдедите доплату за переработку.",
    "price_cold": "Введите доплату за холод.",
    "price_award": "Введите стоимости операции."
}


async def generate_text_of_data(data: dict) -> str:
    """
    Создаем сообщение из текущих настроек пользовател.
    """
    text: str = "Ваши текущие настройки: \n"
    for item in data:
        if "id" not in item:
            text += f"{SETTINGS[item]}: {data[item]}{money}.\n"
    return text


async def get_settings_text(user_id: int) -> str:
    """
    Делаем запрос на существование настроек, если таковые
    имеются, то показываем их.

    :param user_id: Идентификатор пользователя телеграм.
    """
    client = MongoDB()
    collection = client.get_collection("users_settings")
    existing_user: dict = collection.find_one({"user_id": user_id})
    if existing_user:
        return await generate_text_of_data(existing_user)
    return "Выберите какие данные вам нужны."


async def validate_data(action: str, text: str) -> bool | None:
    """
    Проверяем числа на валидность.

    :param action: Команда.
    :param text: Ввод от пользователя.
    """
    if action in SETTINGS:
        return bool(re.match(number_pattern, text))


async def get_settings(user_id: int) -> float:
    """
    Return the user's settings.
    
    :param user_id: The user's ID.
    """
    settings: dict = await get_settings_user_by_id(user_id)
    return (
        float(settings.get("price_overtime", 0)),
        float(settings.get("price_cold", 0))
    )
