from logger import setup_logger

from aiohttp import ClientSession
from os import environ
import os

logger = setup_logger(logger_name=os.path.basename(__file__).split(".")[0])
api_key = str(environ["SOLVER_FUNCTIONS_KEY"])


async def calculate_board_fitness_single(
    board: list, zone_height: int, zone_length: int
) -> tuple:

    """Calculate Board Fitness Single

    This function uses the general solver functions api to calculate and return the total of all the collisions on a given board
    array representation and the board on a single tuple.

    Args:
        board (list): A full filled board representation.
        zone_height (int): The zones height.
        zone_length (int): The zones length.

    Returns:
        int: Total collisions on the board.
        list: The original board.
    """

    body = {"zoneHeight": zone_height, "zoneLength": zone_length, "board": board}
    url = str(environ["FITNESS_SINGLE_SCORE_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with ClientSession(headers=headers) as session:
        async with session.post(url=url, json=body) as response:
            response_body = await response.json()

    return (response_body["fitnessScore"], board)
