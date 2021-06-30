from general_utilities import print_log

import aiohttp
import os

api_key = str(os.environ["SOLVER_FUNCTIONS_KEY"])


async def calculate_and_print_board_fitness_report(
    board: list, zone_height: int, zone_length: int, script_firm: str
) -> None:

    """Calculate And Print Board Fitness Report

    This function uses the general solver functions api to calculate and print a report of all the different
    collisions on a given board array 2D representation.

    Args:
        board (list): A full filled 2D board array representation.
        zone_height (int): The zones height.
        zone_length (int): The zones length.
        script_firm (str): A script firm that is shown on the logs.
    """

    body = {"zone_height": zone_height, "zone_length": zone_length, "board": board}
    url = str(os.environ["FITNESS_REPORT_SCORE_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, json=body) as response:
            response_body = await response.json()

    print_log(f"Errors in board: {str(response_body['total_collisions'])}", script_firm)
    print_log(f"Errors in rows: {str(response_body['row_collisions'])}", script_firm)
    print_log(f"Errors in zones: {str(response_body['zone_collisions'])}", script_firm)
    print_log(
        f"Errors in columns: {str(response_body['column_collisions'])}", script_firm
    )

    return None


async def calculate_board_fitness_report(
    board: list, zone_height: int, zone_length: int
) -> tuple:

    """Calculate Board Fitness Report

    This function uses the general solver functions api to calculate and return all the different collisions
    on a given board array 2D representation.

    Args:
        board (list): A full filled 2D board array representation.
        zone_height (int): The zones height.
        zone_length (int): The zones length.

    Returns:
        int: Total collisions on the board.
        int: Total collisions on the board columns.
        int: Total collisions on the board rows.
        int: Total collisions on the board zones.
    """

    body = {"zone_height": zone_height, "zone_length": zone_length, "board": board}
    url = str(os.environ["FITNESS_REPORT_SCORE_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, json=body) as response:
            response_body = await response.json()

    total_collisions = response_body["total_collisions"]
    column_collisions = response_body["column_collisions"]
    row_collisions = response_body["row_collisions"]
    zone_collisions = response_body["zone_collisions"]

    return total_collisions, column_collisions, row_collisions, zone_collisions


async def calculate_board_fitness_single(
    board: list, zone_height: int, zone_length: int
) -> int:

    """Calculate Board Fitness Single

    This function uses the general solver functions api to calculate and return the total of all the
    collisions on a given board array 2D representation.

    Args:
        board (list): A full filled 2D board array representation.
        zone_height (int): The zones height.
        zone_length (int): The zones length.

    Returns:
        int: Total collisions on the board.
    """

    body = {"zone_height": zone_height, "zone_length": zone_length, "board": board}
    url = str(os.environ["FITNESS_SINGLE_SCORE_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, json=body) as response:
            response_body = await response.json()

    return int(response_body["fitness_score"])


async def board_random_initialization(
    fixed_numbers_board: list, zone_height: int, zone_length: int
) -> list:

    """Board Random Initialization

    This function uses the general solver functions api to fill randomly a board based on its initial state,
    where just the fixed numbers are on the board, the white spaces need to be represented with a 0 and just the
    spaces with 0 are changed for random numbers that are not in the board untill the board is filled.

    Args:
        fixed_numbers_board (list): A 2D board array representation that includes just the fixed numbers.
        zone_height (int): The zones height.
        zone_length (int): The zones length.

    Returns:
        list: A full filled 2D board array representation.
    """

    body = {
        "fixed_numbers_board": fixed_numbers_board,
        "zone_height": zone_height,
        "zone_length": zone_length,
    }
    url = str(os.environ["RANDOM_INITIALIZATION_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, json=body) as response:
            response_body = await response.json()

    return list(response_body["board"])


async def board_random_mutation(board: list, fixed_numbers_board: list) -> list:

    """Board Random Mutation

    This function uses the general solver functions api to mutate randomly a board based on its initial state,
    the mutation affect just the not fixed numbers on the board.

    Args:
        fixed_numbers_board (list): A 2D board array representation that includes just the fixed numbers.
        board (list): A full filled 2D board array representation..

    Returns:
        list: A full filled 2D board array representation with a mutation in one of its rows.
    """

    body = {"fixed_numbers_board": fixed_numbers_board, "board": board}
    url = str(os.environ["RANDOM_MUTATION_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, json=body) as response:
            response_body = await response.json()

    return list(response_body["board"])
