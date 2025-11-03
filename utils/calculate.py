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
