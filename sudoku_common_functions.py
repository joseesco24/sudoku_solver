from logs_printer import print_log
import random


def exchange_two_numbers_from_a_board_row():
    pass


def randomly_start_sudoku_board(
    initial_board: list, sudoku_zone_height: int, sudoku_zone_length: int
) -> list:

    for row in initial_board:
        for column_index in range(len(row)):
            if row[column_index] == 0:
                while True:
                    new_number = random.randrange(
                        1, (sudoku_zone_height * sudoku_zone_length) + 1
                    )
                    if new_number not in row:
                        row[column_index] = new_number
                        break
    return initial_board


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
    print_log(f"Errors in zones: {zone_collisions}", script_firm)
    print_log(f"Errors in rows: {row_collisions}", script_firm)
    print_log(f"Errors in columns: {column_collisions}", script_firm)
