import logging


def setup_logger(logger_name: str) -> logging:

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
