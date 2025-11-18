import json
import asyncio
from datetime import datetime

import aiohttp

from loader import CURRENCY_SYMBOL
from config import cashed_currency
from utils.calculate import calc_valute
from crud.statistics import aggregate_valute

# the address for requesting the ruble exchange rate
URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def request_valute_info() -> str:
    """
    Request information about the ruble exchange rate.
    """
    date = datetime.now()
    current_date: tuple[int] = (date.year, date.month, date.day)
    
    if current_date in cashed_currency:
        return cashed_currency[current_date]
    
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(60)) as client:
        async with client.get(
                url=URL, headers={'Accept': 'application/json'}
        ) as response:
            if response.status == 200:
                currency: dict = json.loads(await response.text())
                cashed_currency.clear()
                cashed_currency[current_date] = currency 
                return currency

            else:
                raise aiohttp.ClientResponseError


async def get_valute_info() -> dict[str, tuple[int, float]]:
    """
    Return the dictionary with information 
    about the value of currencies.
    """
    data = await request_valute_info()
    return {
        "dollar": (
            int(data['Valute']['USD']['Nominal']),
            float(data["Valute"]["USD"]["Value"])
        ),
        "euro": (
            int(data['Valute']['EUR']['Nominal']),
            float(data["Valute"]["EUR"]["Value"])
        ),
        "yena": (
            int(data['Valute']['CNY']['Nominal']),
            float(data["Valute"]["CNY"]["Value"])
        ),
        "som": (
            int(data['Valute']['UZS']['Nominal']),
            float(data["Valute"]["UZS"]["Value"])
        )
    }


async def gen_text(state: dict, name: str) -> str:
    """
    Create a message on earnings in the currency, 
    if you have the data.
    
    :param state: A dictionary with all the data.
    :param name: Name of the currency.
    :return str: A line with information in the selected currency.
    """
    data: dict = await state.get_data()
    current_day: dict = data.get("current_day", {})
    get_sum_valute: float = current_day.get("valute", {}).get(name, 0)
    symbol: str = CURRENCY_SYMBOL[name]
    message = ""

    if  get_sum_valute:
        date_write = str(current_day.get("date_write"))[:10]
        message += f"{get_sum_valute}{symbol}\nПо курсу на {date_write}."
    
    else:
        message = "Нет данных, обновите запись."
    return message


async def get_all_valute_for_month(
    year: int,
    month: int,
    user_id: int
) -> dict:
    """
    Get all currency data for the month.
    
    :return: Combined valute data from all sources.
    """
    data, data_income, data_expence = await asyncio.gather(
        aggregate_valute(year, month, user_id, "salaries"),
        aggregate_valute(year, month, user_id, "other_income"), 
        aggregate_valute(year, month, user_id, "expences")
    )

    return {
        "dollar": data.get("dollar", 0) + \
        data_income.get("dollar", 0) - data_expence.get("dollar", 0),
        "euro": data.get("euro", 0) + \
            data_income.get("euro", 0) - data_expence.get("euro", 0),
        "yena": data.get("yena", 0) + \
            data_income.get("yena", 0) - data_expence.get("yena", 0),
        "som": data.get("som", 0) + \
            data_income.get("som", 0) - data_expence.get("som", 0)
    }


async def get_valute_for_month(
    year: int,
    month: int,
    user_id: int,
    name: str
) -> str:
    """
    Get the currency data.
    
    :param year: The year for the request.
    :param month: The month for the request.
    :param user_id: The user's ID.
    :param state: It is needed to reduce the number of requests.
    :prama name: The name of the currency.
    :param str: A message to the user.
    """
    data = await get_all_valute_for_month(year, month, user_id)
    return f"{data.get(name, 0):,.2f}{CURRENCY_SYMBOL[name]}"


async def get_valute_show_message() -> str:
    """
    Return the line with information about some currencies.
    """
    data = await request_valute_info()
    message = "*" * 40 + "\n\n"
    message += f"Курс рубля на {data["Date"][:10]}.\n\n"
    message += (
        f"{data['Valute']['BYN']['Nominal']}Br "
        f"{data['Valute']['BYN']['Name']}: "
        f"{data['Valute']['BYN']['Value']:.2f}₽.\n"
    )
    message += (
        f"{data['Valute']['USD']['Nominal']}$ "
        f"{data["Valute"]["USD"]["Name"]}: "
        f"{data["Valute"]["USD"]["Value"]:.2f}₽.\n"
    )
    message += (
        f"{data['Valute']['EUR']['Nominal']}€ "
        f"{data["Valute"]["EUR"]["Name"]}: "
        f"{data["Valute"]["EUR"]["Value"]:.2f}₽.\n"
    )
    message += (
        f"{data['Valute']['CNY']['Nominal']}¥ "
        f"{data["Valute"]["CNY"]["Name"]}: "
        f"{data["Valute"]["CNY"]["Value"]:.2f}₽.\n"
    )
    message += (
        f"{data['Valute']['UZS']['Nominal']:,}Soʻm "
        f"{data["Valute"]["UZS"]["Name"]}: "
        f"{data["Valute"]["UZS"]["Value"]:.2f}₽.\n\n"
    )
    message += "*" * 40 + "\n"
    return message
