#include <iostream>

int calculate_board_fitness_single(int board[][20], int board_size, int zone_height, int zone_length)
{

    /*
    This function calculates and returns the summation of all the collisions on a board.

    Args:
        board (list): A full filled board representation.
        zone_height (int): The zones height.
        zone_length (int): The zones length.

    Returns:
        int: Total collisions on the board.
    */

    int collisions = 0;

    for (int row_index = 0; row_index < board_size; row_index++)
    {
        for (int column_index = 0; column_index < board_size; column_index++)
        {
            std::cout << board[row_index][column_index];
        }
    }

    /*
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
    */

    return collisions;
}