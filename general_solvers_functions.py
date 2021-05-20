from general_utility_functions import print_log

from copy import deepcopy
import random


def exchange_two_numbers_from_a_current_board_row(
    filled_board: list, fixed_numbers_board: list
) -> list:

    row_index = random.randrange(len(filled_board))

    while True:
        column_index_1 = random.randrange(len(filled_board[row_index]))
        if fixed_numbers_board[row_index][column_index_1] == 0:
            number_1 = deepcopy(filled_board[row_index][column_index_1])
            break

    while True:
        column_index_2 = random.randrange(len(filled_board[row_index]))
        if fixed_numbers_board[row_index][column_index_2] == 0:
            number_2 = deepcopy(filled_board[row_index][column_index_2])
            break

    filled_board[row_index][column_index_1] = number_2
    filled_board[row_index][column_index_2] = number_1

    return filled_board


def randomly_start_the_board(
    fixed_numbers_board: list, zone_height: int, zone_length: int
) -> list:

    filled_board = deepcopy(fixed_numbers_board)

    for row_index in range(len(filled_board)):
        for column_index in range(len(filled_board[row_index])):
            if filled_board[row_index][column_index] == 0:
                while True:
                    new_number = random.randrange(1, (zone_height * zone_length) + 1)
                    if new_number not in filled_board[row_index]:
                        filled_board[row_index][column_index] = new_number
                        break

    return filled_board


def calculate_sudoku_board_fitness_score(
    board: list, zone_height: int, zone_length: int
) -> int:

    collisions = 0

    for row in range(len(board)):
        row_set = set()
        for column in range(len(board[row])):
            row_set.add(board[row][column])
        row_repetitions = abs(len(board[row]) - len(row_set))
        collisions += row_repetitions

    for row in range(len(board)):
        column_set = set()
        for column in range(len(board[row])):
            column_set.add(board[column][row])
        column_repetitions = abs(len(board[row]) - len(column_set))
        collisions += column_repetitions

    for row in range(0, len(board), zone_height):
        for column in range(0, len(board[row]), zone_length):
            zone_set = set()
            for i in range(zone_height):
                sub1 = board[row + i][column : column + zone_length]
                zone_set.update(set(sub1))
            zone_repetitions = abs((zone_length * zone_height) - len(zone_set))
            collisions += zone_repetitions

    return collisions


def print_sudoku_board_collisions_report(
    board: list, zone_height: int, zone_length: int, script_firm: str
) -> None:

    row_collisions, column_collisions, zone_collisions = 0, 0, 0

    for row in range(len(board)):
        row_set = set()
        for column in range(len(board[row])):
            row_set.add(board[row][column])
        row_repetitions = abs(len(board[row]) - len(row_set))
        row_collisions += row_repetitions

    for row in range(len(board)):
        column_set = set()
        for column in range(len(board[row])):
            column_set.add(board[column][row])
        column_repetitions = abs(len(board[row]) - len(column_set))
        column_collisions += column_repetitions

    for row in range(0, len(board), zone_height):
        for column in range(0, len(board[row]), zone_length):
            zone_set = set()
            for i in range(zone_height):
                sub1 = board[row + i][column : column + zone_length]
                zone_set.update(set(sub1))
            zone_repetitions = abs((zone_length * zone_height) - len(zone_set))
            zone_collisions += zone_repetitions

    total_collisions = zone_collisions + row_collisions + column_collisions

    print_log(f"Errors in board: {total_collisions}", script_firm)
    print_log(f"Errors in rows: {row_collisions}", script_firm)
    print_log(f"Errors in zones: {zone_collisions}", script_firm)
    print_log(f"Errors in columns: {column_collisions}", script_firm)
