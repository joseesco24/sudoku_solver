from general_solvers_functions import exchange_two_numbers_from_a_current_board_row
from general_solvers_functions import print_board_collisions_report
from general_solvers_functions import calculate_board_fitness_score
from general_solvers_functions import randomly_start_the_board
from general_utility_functions import normalize_decimal
from general_utility_functions import print_log

from copy import deepcopy
from time import time
import itertools
import random

script_firm = "grs"


def exchange_if_sudoku_board_improves(
    filled_board: list, fixed_numbers_board: list, zone_height: int, zone_length: int
) -> list:

    initial_board = deepcopy(filled_board)
    current_board = deepcopy(filled_board)

    current_board = exchange_two_numbers_from_a_current_board_row(
        filled_board=current_board, fixed_numbers_board=fixed_numbers_board
    )

    current_board_fitness = calculate_board_fitness_score(
        board=current_board, zone_height=zone_height, zone_length=zone_length
    )
    initial_board_fitness = calculate_board_fitness_score(
        board=initial_board, zone_height=zone_height, zone_length=zone_length
    )

    if current_board_fitness <= initial_board_fitness:
        return current_board
    else:
        return initial_board


def solve_using_hill_climbing_algorithm(
    hill_climbing_restarts: int,
    hill_climbing_searchs: int,
    zone_height: int,
    zone_length: int,
    board: list,
) -> list:

    fixed_numbers_board = deepcopy(board)

    print_log(r"starting to solve with hill climbing algorithm", script_firm)

    restarts_counter, searches_counter = 0, 0
    boards_list = list()
    start_time = time()

    for _ in itertools.repeat(None, hill_climbing_restarts):
        restarts_counter += 1
        filled_board = randomly_start_the_board(
            fixed_numbers_board=fixed_numbers_board,
            zone_height=zone_height,
            zone_length=zone_length,
        )

        for _ in itertools.repeat(None, hill_climbing_searchs):
            searches_counter += 1
            filled_board = exchange_if_sudoku_board_improves(
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
        best_board_fitness = calculate_board_fitness_score(
            board=best_board, zone_height=zone_height, zone_length=zone_length
        )
        current_board_fitness = calculate_board_fitness_score(
            board=current_board, zone_height=zone_height, zone_length=zone_length
        )
        if current_board_fitness < best_board_fitness:
            best_board = current_board

    print_board_collisions_report(
        zone_height=zone_height,
        zone_length=zone_length,
        script_firm=script_firm,
        board=best_board,
    )

    return best_board
