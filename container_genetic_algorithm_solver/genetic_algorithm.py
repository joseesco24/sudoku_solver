from general_solver_functions_access import calculate_board_fitness_single
from general_solver_functions_access import board_random_initialization
from general_solver_functions_access import board_random_mutation

from general_utilities import normalize_decimal
from general_utilities import print_log

from asyncio import gather
from copy import deepcopy
from time import time
import itertools
import random

script_firm = "gas"


async def mutate_if_sudoku_board_improves(
    filled_board: list, fixed_numbers_board: list, zone_height: int, zone_length: int
) -> list:

    initial_board = deepcopy(filled_board)
    current_board = deepcopy(filled_board)

    current_board = await board_random_mutation(
        board=current_board, fixed_numbers_board=fixed_numbers_board
    )

    current_board_fitness, initial_board_fitness = await gather(
        calculate_board_fitness_single(
            board=current_board, zone_height=zone_height, zone_length=zone_length
        ),
        calculate_board_fitness_single(
            board=initial_board, zone_height=zone_height, zone_length=zone_length
        ),
    )

    if current_board_fitness <= initial_board_fitness:
        return current_board
    else:
        return initial_board


async def solve_using_genetic_algorithm(
    genetic_algorithm_crossover: float,
    genetic_algorithm_generations: int,
    genetic_algorithm_population: int,
    genetic_algorithm_mutation: float,
    zone_height: int,
    zone_length: int,
    board: list,
) -> list:

    print_log(
        f"{genetic_algorithm_crossover}, {genetic_algorithm_mutation}", script_firm
    )

    fixed_numbers_board = deepcopy(board)

    print_log(r"starting to solve with hill climbing algorithm", script_firm)

    restarts_counter, searches_counter = 0, 0
    boards_list = list()
    start_time = time()

    for _ in itertools.repeat(None, genetic_algorithm_generations):
        restarts_counter += 1
        filled_board = await board_random_initialization(
            fixed_numbers_board=fixed_numbers_board,
            zone_height=zone_height,
            zone_length=zone_length,
        )

        for _ in itertools.repeat(None, genetic_algorithm_population):
            searches_counter += 1
            filled_board = await mutate_if_sudoku_board_improves(
                fixed_numbers_board=fixed_numbers_board,
                filled_board=filled_board,
                zone_height=zone_height,
                zone_length=zone_length,
            )
            boards_list.append(filled_board)

    end_time = time()
    elapsed_time = end_time - start_time

    print_log(r"finishing to solve with hill climbing algorithm", script_firm)

    print_log(f"total restarts: {restarts_counter}", script_firm)
    print_log(f"total searches: {searches_counter}", script_firm)

    print_log(
        f"time spent searching a solution: {normalize_decimal(elapsed_time)}s",
        script_firm,
    )

    best_board = random.choice(boards_list)

    for current_board in boards_list:
        best_board_fitness, current_board_fitness = await gather(
            calculate_board_fitness_single(
                board=best_board, zone_height=zone_height, zone_length=zone_length
            ),
            calculate_board_fitness_single(
                board=current_board, zone_height=zone_height, zone_length=zone_length
            ),
        )
        if current_board_fitness < best_board_fitness:
            best_board = current_board

    return best_board
