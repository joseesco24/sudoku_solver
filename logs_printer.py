from datetime import datetime


def print_log(message: str, script_firm: str = None) -> None:

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = str(message).capitalize()

    if script_firm is not None:
        print(f"[{date_time}][{script_firm}] - {message}")

    else:
        print(f"[{date_time}] - {message}")
