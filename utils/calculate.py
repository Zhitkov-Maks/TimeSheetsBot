async def calc_valute(
    earned: float,
    valute_data: dict[str, tuple[int, float]]
) -> dict[str, float]:
    """
    Calculate the amount of earnings in currencies.

    :param earned: Earnings per day.
    :param valute_data: Information about the ruble exchange rate.
    :return dict: Dictionary where the key is the name of the currency, 
                    the value is the calculated value.
    """
    earned_in_valute: dict[str, float] = {}
    for key, value in valute_data.items():
        earned_in_valute.update(
            {
                key: round(earned * value[0] / value[1], 2)
            }
        )
    return earned_in_valute


async def calculation_by_part(data: dict) -> tuple[float]:
    """
    Return the tuple with the necessary data.

    :param data: A dictionary with input data.
    :return list: A list with calculation data.
    """
    earned: float = data.get("total_earned", 0)
    hours: float = data.get("total_base_hours", 0)
    earned_hours: float = data.get("total_earned_hours", 0)
    award: float = data.get("total_award", 0)
    count_operations: float = data.get("total_operations", 0)
    earned_cold: float = data.get("total_earned_cold", 0)
    overtime_money: float = data.get("total_overitme", 0)
    overtime_hours: float = data.get("total_hours_overitme", 0)
    return (
        earned,
        hours,
        award,
        count_operations,
        earned_cold,
        earned_hours,
        overtime_money,
        overtime_hours
    )


async def data_calculation(
    data: tuple
) -> list[tuple | float]:
    """
    Collect the data for further work with them.
    
    :param data: A tuple with data.
    :return list: A list with data.
    """
    period_1: tuple = await calculation_by_part(data[0])
    period_2: tuple = await calculation_by_part(data[1])

    hours: float = period_1[1] + period_2[1]
    income: float = data[2].get("total_sum", 0)
    expense: float = data[3].get("total_sum", 0)
    award: float = period_1[2] + period_2[2]
    earned_cold = period_1[4] + period_2[4]
    operations: float = period_1[3] + period_2[3]
    total_earned: float = (
        period_1[0] + period_2[0] + income - expense
    )
    return [
        period_1,
        period_2,
        income,
        expense,
        award,
        operations,
        total_earned,
        hours,
        earned_cold
    ]


async def generate_data(
    data: list,
    p1: tuple,
    p2: tuple
) -> tuple:
    """Form the tuple in the correct order for the 
    subsequent generation of the message to the user.
    
    :param data: A list with data.
    :param p1: Information for the first period.
    :param p2: Information for the second period.
    """
    return (
        data[6], # Всего заработано.
        data[7], # Часов отработано.
        data[4], # Премия.
        data[5], # Кол-во операций.
        p1[4] + p2[4], # За холод.
        p1[5] + p2[5], # Заработано за часы.
        p1[6] + p2[6], # Заработано за переработки.
        p2[7] + p1[7], # Часов переработки
        data[2], # Прочие доходы.
        data[3] # Вычеты.
    )
