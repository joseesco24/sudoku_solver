from os import path
from os import walk
import os

script_path = os.path.basename(__file__)
directory_path = os.getcwd()

results_path_boards = path.join(directory_path, "results", "boards")

zone_dimensions = (3, 3)


def get_file_name(board_path):
    return path.basename(board_path).split(".")[0]


def read_initial_board(board_path):
    board_a = []
    archivo = open(board_path, "r")
    lineas = list(archivo)
    for linea in lineas:
        linea = linea.split(" ")
        linea = [x for x in filter(lambda x: x != "\n", linea)]
        for i in range(len(linea)):
            linea[i] = int(linea[i])
        board_a.append(linea)
    archivo.close()
    return board_a


def custom_fitness_report(individual):
    row_collisions, column_collisions, zone_collisions = 0, 0, 0

    for row in range(len(individual)):
        row_set = set()
        for column in range(len(individual[row])):
            row_set.add(individual[row][column])
        repetitions = abs(len(individual[row]) - len(row_set))
        row_collisions += repetitions

    for row in range(len(individual)):
        column_set = set()
        for column in range(len(individual[row])):
            column_set.add(individual[column][row])
        column_repetitions = abs(len(individual[row]) - len(column_set))
        column_collisions += column_repetitions

    for row in range(0, len(individual), zone_dimensions[-1]):
        for column in range(0, len(individual[row]), zone_dimensions[0]):
            zone_set = set()
            for i in range(zone_dimensions[-1]):
                sub1 = individual[row + i][column : column + zone_dimensions[0]]
                zone_set.update(set(sub1))
            zone_repetitions = abs(
                (zone_dimensions[0] * zone_dimensions[-1]) - len(zone_set)
            )
            zone_collisions += zone_repetitions

    print("errors in zones: " + str(zone_collisions))
    print("errors in rows: " + str(row_collisions))
    print("erros in columns: " + str(column_collisions))


def custom_fitness(individual):
    collisions = 0

    for row in range(len(individual)):
        column_set = set()
        for column in range(len(individual[row])):
            column_set.add(individual[column][row])
        column_repetitions = abs(len(individual[row]) - len(column_set))
        collisions += column_repetitions

    for row in range(0, len(individual), zone_dimensions[-1]):
        for column in range(0, len(individual[row]), zone_dimensions[0]):
            zone_set = set()
            for i in range(zone_dimensions[-1]):
                sub1 = individual[row + i][column : column + zone_dimensions[0]]
                zone_set.update(set(sub1))
            zone_repetitions = abs(
                (zone_dimensions[0] * zone_dimensions[-1]) - len(zone_set)
            )
            collisions += zone_repetitions

    return collisions


if path.exists(results_path_boards):

    all_files_list = [file_name for _, _, file_name in walk(results_path_boards)][0]
    txt_files_list = [
        file_name
        for file_name in filter(
            lambda file_name: file_name.split(".")[-1] == "txt", all_files_list
        )
    ]

    print("")
    for file_name in txt_files_list:

        board_path = path.join(results_path_boards, file_name)
        board_a = read_initial_board(board_path)
        board_name = get_file_name(board_path)

        print(f"evaluating with: {get_file_name(script_path)}")
        print(f"board name: {board_name}")
        print(f"board path: {board_path}")
        print(f"errors: {custom_fitness(board_a)}")
        custom_fitness_report(board_a)

        print("")
