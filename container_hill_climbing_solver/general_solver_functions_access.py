from general_utilities import print_log

import aiohttp
import os

api_key = str(os.environ["SOLVER_FUNCTIONS_KEY"])


async def calculate_and_print_board_fitness_report(
    board: list, zone_height: int, zone_length: int, script_firm: str
) -> None:

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

    body = {"fixed_numbers_board": fixed_numbers_board, "board": board}
    url = str(os.environ["RANDOM_MUTATION_LINK"])
    response_body = dict()

    headers = {"Authorization": api_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, json=body) as response:
            response_body = await response.json()

    return list(response_body["board"])
