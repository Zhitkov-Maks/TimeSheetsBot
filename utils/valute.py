import json

import aiohttp

from loader import CURRENCY_SYMBOL
from utils import current_day
from utils.calculate import calc_valute

# the address for requesting the ruble exchange rate
URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def request_valute_info() -> str:
    """
    Request information about the ruble exchange rate.
    """
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(60)) as client:
        async with client.get(
                url=URL, headers={'Accept': 'application/json'}
        ) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise aiohttp.ClientResponseError

                
async def get_valute_info() -> dict[str, tuple[int, float]]:
    """
    Return the dictionary with information 
    about the value of currencies.
    """
    data = json.loads(await request_valute_info())
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
