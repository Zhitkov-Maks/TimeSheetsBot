import re

from keyboards.settings import SETTINGS
from database.db_conf import MongoDB
from loader import money

number_pattern = r'^-?\d+(\.\d+)?$'

actions_dict: dict[str, tuple] = {
    "price_time": "Введите вышу почасовую оплату труда.",
    "price_overtime": "Ввдедите доплату за переработку.",
    "price_line": "Введите стоимость оплаты строки.",
    "number_hours_per_month": "Норма часов за месяц",
    "price_cold": "Введите доплату за холод",
    "price_line_over": "Введите стоимость строки, если строчек больше нормы.",
    "count_line": "Введите норму строк, для оплаты по повышенной ставке."
}


async def generate_text_of_data(data: dict) -> str:
    """
    Создаем сообщение из текущих настроек пользовател.
    """
    text: str = "Ваши текущие настройки: "
    for item in data:
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
        return await generate_text_of_data(existing_user.get("data"))
    return "Выберите какие данные вам нужны."


async def validate_data(action: str, text: str) -> bool | None:
    """
    Проверяем числа на валидность.
    :param action: Команда.
    :param text: Ввод от пользователя.
    """
    if action in SETTINGS:
        return bool(re.match(number_pattern, text))


async def create_settings(data: dict, user_id: int) -> None:
    """
    Создание или обновление настроек пользователя.

    :param data: Словарь с введенными данными.
    :param user_id: Идентификатор пользователя.
    """
    client = MongoDB()
    collection = client.get_collection("users_settings")
    collection.update_one(
        {"user_id": user_id}, {"$set": {"data": data}}, upsert=True
    )
    client.close()
