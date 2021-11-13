import logging


def setup_logger(logger_name: str) -> logging:

    """Setup Logger

    This function is used to obtain a logging object in anny function.

    Args:
        logger_name (str): The logger name.

    Returns:
        logging: The new logger.
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s]:%(levelname)s:%(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def get_board_stamp(board: list) -> str:

    board_stamp = ""

    for row in board:
        for element in row:
            board_stamp += str(element)

    return "|" + board_stamp + "|"
