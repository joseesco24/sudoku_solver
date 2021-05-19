from logs_printer import print_log


def print_board_collisions_report(
    board: list, zone_dimensions: tuple, script_firm: str
) -> None:

    row_collisions, column_collisions, zone_collisions = 0, 0, 0

    for row in range(len(board)):
        row_set = set()
        for column in range(len(board[row])):
            row_set.add(board[row][column])
        repetitions = abs(len(board[row]) - len(row_set))
        row_collisions += repetitions

    for row in range(len(board)):
        column_set = set()
        for column in range(len(board[row])):
            column_set.add(board[column][row])
        column_repetitions = abs(len(board[row]) - len(column_set))
        column_collisions += column_repetitions

    for row in range(0, len(board), zone_dimensions[-1]):
        for column in range(0, len(board[row]), zone_dimensions[0]):
            zone_set = set()
            for i in range(zone_dimensions[-1]):
                row_subset = board[row + i][column : column + zone_dimensions[0]]
                zone_set.update(set(row_subset))
            zone_repetitions = abs(
                (zone_dimensions[0] * zone_dimensions[-1]) - len(zone_set)
            )
            zone_collisions += zone_repetitions

    total_errors = zone_collisions + row_collisions + column_collisions

    print_log(f"Errors in board: {total_errors}", script_firm)
    print_log(f"Errors in zones: {zone_collisions}", script_firm)
    print_log(f"Errors in rows: {row_collisions}", script_firm)
    print_log(f"Errors in columns: {column_collisions}", script_firm)
