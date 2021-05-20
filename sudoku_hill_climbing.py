from sudoku_common_functions import exchange_two_numbers_from_a_current_board_row
from sudoku_common_functions import print_sudoku_board_collisions_report
from sudoku_common_functions import calculate_sudoku_board_fitness_score
from sudoku_common_functions import randomly_start_the_board

from logs_printer import print_log

from copy import deepcopy
from time import time
import random

script_firm = "hcs"


def exchange_if_sudoku_board_improves(
    current_board: list, initial_board: list, zone_height: int, zone_length: int
) -> list:
    current_board = exchange_two_numbers_from_a_current_board_row(
        current_board=current_board, initial_board=initial_board
    )
    current_board_fitness = calculate_sudoku_board_fitness_score(
        board=current_board, zone_height=zone_height, zone_length=zone_length
    )
    initial_board_fitness = calculate_sudoku_board_fitness_score(
        board=initial_board, zone_height=zone_height, zone_length=zone_length
    )
    if current_board_fitness > initial_board_fitness:
        return current_board
    else:
        return initial_board


def solve_sudoku_using_hill_climbing_algorithm(
    board: list,
    zone_height: int,
    zone_length: int,
    hill_climbing_restarts: int = 1,
    hill_climbing_searchs: int = 10,
) -> list:

    initial_board_l1 = deepcopy(board)
    current_board_l1 = deepcopy(board)

    print_log("starting to solve with hill climbing algorithm", script_firm)

    boards_list = list()
    start_time = time()

    for _ in range(hill_climbing_restarts + 1):

        current_board_l1 = randomly_start_the_board(
            initial_board=initial_board_l1,
            zone_height=zone_height,
            zone_length=zone_length,
        )

        for _ in range(hill_climbing_searchs + 1):

            current_board_l1 = exchange_if_sudoku_board_improves(
                current_board=current_board_l1,
                initial_board=initial_board_l1,
                zone_height=zone_height,
                zone_length=zone_length,
            )

            boards_list.append(current_board_l1)

    end_time = time()
    elapsed_time = end_time - start_time

    print_log("finishing to solve with hill climbing algorithm", script_firm)
    print_log(f"time spent searching a solution: {elapsed_time} seconds", script_firm)

    best_board = random.choice(boards_list)

    for board in boards_list:
        best_board_fitness = calculate_sudoku_board_fitness_score(
            board=best_board, zone_height=zone_height, zone_length=zone_length
        )
        board_fitness = calculate_sudoku_board_fitness_score(
            board=board, zone_height=zone_height, zone_length=zone_length
        )
        if board_fitness < best_board_fitness:
            best_board = board

    print_sudoku_board_collisions_report(
        zone_height=zone_height,
        zone_length=zone_length,
        script_firm=script_firm,
        board=best_board,
    )

    return best_board
