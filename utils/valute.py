import json

import aiohttp


URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def request_valute_info() -> str:
    """Запроси данные о курсе рубля."""
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(60)) as client:
        async with client.get(
                url=URL, headers={'Accept': 'application/json'}
        ) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise aiohttp.ClientResponseError

                
async def get_valute_info() -> str:
    """
    Верни строку с информацией о некоторых валутах.
    """
    data = json.loads(await request_valute_info())
    message = "*" * 40 + "\n\n"
    message += f"Курс рубля на {data["Date"][:10]}.\n\n"
    message += (
        f"{data["Valute"]["BYN"]["Name"]}: {data["Valute"]["BYN"]["Value"]}Br.\n"
    )
    message += (
        f"{data["Valute"]["USD"]["Name"]}: {data["Valute"]["USD"]["Value"]}$.\n"
    )
    message += (
        f"{data["Valute"]["EUR"]["Name"]}: {data["Valute"]["EUR"]["Value"]}€.\n"
    )
    message += (
        f"{data["Valute"]["CNY"]["Name"]}: {data["Valute"]["BYN"]["Value"]}¥.\n"
    )
    message += (
        f"{data["Valute"]["UZS"]["Name"]}: "
        f"{
            round(
                data["Valute"]["UZS"]["Value"] /
                data["Valute"]["UZS"]["Nominal"], 5
            )
        }Soʻm.\n\n"
    )
    message += "*" * 40 + "\n"
    return message
