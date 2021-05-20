from logs_printer import print_log

from copy import deepcopy
import random


def exchange_two_numbers_from_a_current_board_row(
    current_board: list, initial_board: list
) -> list:

    row_index = random.randrange(len(current_board))
    column_index_1, column_index_2 = 0, 0
    number_1, number_2 = 0, 0

    while True:
        column_index_1 = random.randrange(len(current_board[row_index]))
        number_1 = initial_board[row_index][column_index_1]
        if number_1 == 0:
            break

    while True:
        column_index_2 = random.randrange(len(current_board[row_index]))
        number_2 = initial_board[row_index][column_index_2]
        if number_2 == 0:
            break

    current_board[row_index][column_index_1] = number_2
    current_board[row_index][column_index_2] = number_1

    return current_board


def randomly_start_the_board(
    initial_board: list, zone_height: int, zone_length: int
) -> list:

    board = deepcopy(initial_board)

    for row_index in range(len(board)):
        for column_index in range(len(board[row_index])):
            if board[row_index][column_index] == 0:
                while True:
                    new_number = random.randrange(1, (zone_height * zone_length) + 1)
                    if new_number not in board[row_index]:
                        board[row_index][column_index] = new_number
                        break

    return board


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

    for row in range(0, len(board), zone_length):
        for column in range(0, len(board[row]), zone_height):
            zone_set = set()
            for i in range(zone_length):
                sub1 = board[row + i][column : column + zone_height]
                zone_set.update(set(sub1))
            zone_repetitions = abs((zone_height * zone_length) - len(zone_set))
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

    for row in range(0, len(board), zone_length):
        for column in range(0, len(board[row]), zone_height):
            zone_set = set()
            for i in range(zone_length):
                row_subset = board[row + i][column : column + zone_height]
                zone_set.update(set(row_subset))
            zone_repetitions = abs((zone_height * zone_length) - len(zone_set))
            zone_collisions += zone_repetitions

    total_collisions = zone_collisions + row_collisions + column_collisions

    print_log(f"Errors in board: {total_collisions}", script_firm)
    print_log(f"Errors in rows: {row_collisions}", script_firm)
    print_log(f"Errors in zones: {zone_collisions}", script_firm)
    print_log(f"Errors in columns: {column_collisions}", script_firm)
