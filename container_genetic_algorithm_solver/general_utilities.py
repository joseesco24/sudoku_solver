from datetime import datetime


def print_log(message: str, script_firm: str = None) -> None:

    """Print Log Function

    This functions is in charge of printing all the necessary logs of the application with the same format.

    Args:
        message (str): Any message that needs to be printed with a log format.
        script_firm (str = None): The script firm that indicates where the message comes.
    """

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = str(message).capitalize()
    if script_firm is not None:
        script_firm = script_firm.upper()
        print(f"[{date_time}][{script_firm}] - {message}")
    else:
        print(f"[{date_time}] - {message}")


def normalize_decimal(decimal: float) -> float:

    """Normalize Decimal Function

    This is a simple function that helps normalizing float numbers rounding it to just four decimals.

    Args:
        decimal (float): Any float number.

    Returns:
        float: A float number rounded to just dour decimals.
    """

    return round(decimal, 4)
