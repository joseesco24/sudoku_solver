from copy import deepcopy
import random


def calculate_board_fitness_single(
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


def calculate_board_fitness_report(
    board: list, zone_height: int, zone_length: int
) -> list:

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

    return total_collisions, zone_collisions, row_collisions, column_collisions


def board_random_initialization(
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


def board_random_mutation(board: list, fixed_numbers_board: list) -> list:

    row_index = random.randrange(len(board))

    while True:
        column_index_1 = random.randrange(len(board[row_index]))
        if fixed_numbers_board[row_index][column_index_1] == 0:
            number_1 = deepcopy(board[row_index][column_index_1])
            break

    while True:
        column_index_2 = random.randrange(len(board[row_index]))
        if fixed_numbers_board[row_index][column_index_2] == 0:
            number_2 = deepcopy(board[row_index][column_index_2])
            break

    board[row_index][column_index_1] = number_2
    board[row_index][column_index_2] = number_1

    return board
