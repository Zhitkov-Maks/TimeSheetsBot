from datetime import datetime as dt

from aiogram.utils.markdown import hbold

from config import month_tuple, weekdays


async def generate_str(iterable, month: int, period) -> str:
    """
    Генерация сообщения с подробной информацией на каждый
    день об отработанных часах и заработанной сумме.
    """
    if period != 0:
        create_str: str = (
            f"\n{"Подробный отчет за"} "
            f"{hbold(month_tuple[month])}\n"
            f"{hbold("Период:", period)}\n{'-' * 60}")
    else:
        create_str = f"{
            hbold("Итог за ", month_tuple[month])
        }\n{60*"-"}"

    total_salary: float = 0
    total_hours: float = 0
    hours_overtime: float = 0

    for sal in iterable:
        if sal[0].period == period:
            total_salary += sal[0].earned
            hours_all_day = round(sal[0].base_hours + sal[0].overtime, 2)
            hours_overtime += sal[0].overtime

            total_hours += hours_all_day
            day, month, year = sal[0].date.split("/")

            weekday = dt(int(year), int(month), int(day)).weekday()
            create_str += (
                f"\n<b>Дата - {sal[0].date[:5]} ({weekdays[weekday]}) => "
                f"{round(hours_all_day, 2)} ч / "
                f"{sal[0].earned}₽</b>\n{'-' * 60}"
            )

        elif period == 0:
            total_salary += sal[0].earned
            hours_all_day = round(sal[0].base_hours + sal[0].overtime, 2)
            hours_overtime += sal[0].overtime

            total_hours += hours_all_day

    create_str += f"\n{hbold("Итого имеем")} 💵💴💶💶💷\n" if period else "\n"
    create_str += f"Заработано - {hbold(total_salary)}₽\n"
    create_str += f"Отработано часов - {hbold(total_hours)} ч\n"
    create_str += f"Из них доп часов {hbold(hours_overtime)} ч \n"

    return create_str
