from sudoku_common_functions import check_and_correct_one_sudoku_board_row
from sudoku_common_functions import calculate_sudoku_board_fitness_score
from sudoku_common_functions import randomly_start_sudoku_board

from copy import deepcopy
from time import time
import random

script_firm = "hc"


def mutate_if_sudoku_board_improves(
    sudoku_board: int, sudoku_zone_height, sudoku_zone_length
):

    current_board = deepcopy(sudoku_board)
    initial_board = deepcopy(sudoku_board)

    row_index = random.randrange(len(initial_board))

    column_index_1 = random.randrange(len(initial_board[row_index]))
    column_index_2 = random.randrange(len(initial_board[row_index]))

    current_board[row_index][column_index_1] = initial_board[row_index][column_index_2]
    current_board[row_index][column_index_2] = initial_board[row_index][column_index_1]

    current_board = check_and_correct_one_sudoku_board_row(current_board, row_index)

    current_board_fitness = calculate_sudoku_board_fitness_score(current_board)
    initial_board_fitness = calculate_sudoku_board_fitness_score(initial_board)

    if current_board_fitness > initial_board_fitness:
        return current_board
    else:
        return initial_board


def solve_sudoku_using_hill_climbing_algorithm(
    sudoku_initial_board: list,
    sudoku_zone_height: int,
    sudoku_zone_length: int,
    hill_climbing_restarts: int = 1,
    hill_climbing_searchs: int = 10,
):

    initial_board = deepcopy(sudoku_initial_board)
    current_board = deepcopy(sudoku_initial_board)

    boards_list = list()

    start_time = time()

    for _ in range(hill_climbing_restarts + 1):
        current_board = randomly_start_sudoku_board(
            initial_board, sudoku_zone_height, sudoku_zone_length
        )

        for _ in range(hill_climbing_searchs + 1):
            current_board = mutate_if_sudoku_board_improves(
                current_board, sudoku_zone_height, sudoku_zone_length
            )
            boards_list.append(current_board)

    end_time = time()
    elapsed_time = end_time - start_time

    best_board = random.choice(boards_list)

    for board in boards_list:
        if calculate_sudoku_board_fitness_score(
            board
        ) < calculate_sudoku_board_fitness_score(best_board):
            best_board = board
