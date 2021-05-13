import matplotlib.pyplot as plt
from operator import attrgetter
from pyeasyga import pyeasyga
from copy import deepcopy
from time import time
from os import path
from os import walk
import random
import sys
import os

script_path = path.basename(__file__)
directory_path = os.getcwd()

boards_path = path.join(directory_path, "boards")
results_path_images = path.join(directory_path, "results", "images")
results_path_boards = path.join(directory_path, "results", "boards")

if not path.exists(boards_path):
    os.makedirs(boards_path)
if not path.exists(results_path_images):
    os.makedirs(results_path_images)
if not path.exists(results_path_boards):
    os.makedirs(results_path_boards)

zone_dimensions = (3, 3)

generations = 10
population = 100

parents_selection_option = 1
crossover_probability = 0.8
mutation_probability = 0.2
elitism_setup = True

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    for argument_index in range(len(arguments)):
        if argument_index < (len(arguments) - 1):
            argument_value = arguments[argument_index]
            if argument_value == "--generations":
                generations = int(arguments[argument_index + 1])
            if argument_value == "--population":
                population = int(arguments[argument_index + 1])
            if argument_value == "--restarts":
                restarts = int(arguments[argument_index + 1])
            if argument_value == "--searchs":
                searchs = int(arguments[argument_index + 1])


def get_file_name(board_path):
    return path.basename(board_path).split(".")[0]


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


def custom_fitness(individual, _):
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


def custom_creation(data):
    for row in data:
        for index in range(len(row)):
            if row[index] == 0:
                while True:
                    new_number = random.randrange(
                        1, (zone_dimensions[0] * zone_dimensions[-1]) + 1
                    )
                    if new_number not in row:
                        break
                row[index] = new_number
    return data


def tournament_selection(population):
    tournment_size = len(population) // 2
    if tournment_size == 0:
        tournment_size = 2
    participant_members = random.sample(population, tournment_size)
    participant_members.sort(key=attrgetter("fitness"), reverse=False)
    return participant_members[0]


def roulette_selection(population):
    roulette = list()
    for individual in population:
        fitness = int(individual.fitness)
        if fitness == 0:
            prob = 100
        if fitness != 0:
            prob = int(100 / fitness)
        roulette.extend([individual] * prob)
    random.shuffle(roulette)
    return random.choice(roulette)


def random_selection(population):
    return random.choice(population)


def correct_row(individual, fi1):
    global board_b
    for col1 in range(len(board_b[fi1])):
        if board_b[fi1][col1] != 0 and individual[fi1][col1] != board_b[fi1][col1]:
            col2 = individual[fi1].index(board_b[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = (
                individual[fi1][col2],
                individual[fi1][col1],
            )
    return individual


def custom_mutation(individual):
    if1 = random.randrange(len(individual))
    ic1 = random.randrange(len(individual[if1]))
    ic2 = random.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = (
        individual[if1][ic2],
        individual[if1][ic1],
    )
    return correct_row(individual, if1)


def save_board(board, output_file_path):

    if path.exists(output_file_path):
        os.remove(output_file_path)

    for row in board:
        with open(output_file_path, "a") as output_file:
            for number in row:
                output_file.write(f"{number} ")
            output_file.write("\n")


def custom_crossover(parent_1, parent_2):
    if1 = random.randrange(len(parent_1))
    if2 = random.randrange(len(parent_1))
    parent_1[if1], parent_2[if2] = parent_2[if2], parent_1[if1]
    return correct_row(parent_1, if1), correct_row(parent_2, if2)


def get_average_fitness(ga):
    fitness_po = [i.fitness for i in ga.current_generation]
    average = sum(fitness_po) / len(fitness_po)
    return format(average)


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


all_files_list = [file_name for _, _, file_name in walk(boards_path)][0]
txt_files_list = [
    file_name
    for file_name in filter(
        lambda file_name: file_name.split(".")[-1] == "txt", all_files_list
    )
]

print("")
for file_name in txt_files_list:

    board_path = path.join(boards_path, file_name)
    board_name = get_file_name(board_path)
    board_a = read_initial_board(board_path)
    board_b = deepcopy(board_a)

    y_axis_0 = list()
    y_axis_1 = list()
    x_axis_0 = list()

    generations_counter = 0

    print(f"solving with: {get_file_name(script_path)}")
    print(f"board name: {board_name}")
    print(f"board path: {board_path}")

    ga = pyeasyga.GeneticAlgorithm(
        seed_data=board_a,
        population_size=population,
        crossover_probability=crossover_probability,
        mutation_probability=mutation_probability,
        elitism=elitism_setup,
        maximise_fitness=False,
    )

    ga.create_individual = custom_creation
    ga.crossover_function = custom_crossover
    ga.mutate_function = custom_mutation
    ga.selection_function = [
        tournament_selection,
        roulette_selection,
        random_selection,
    ][parents_selection_option]
    ga.fitness_function = custom_fitness
    ga.create_first_generation()

    print("starting to solve the board")
    start_time = time()

    for i in range(generations + 1):
        print(f"elapsed generations: {i}/{generations}", end="\r")
        ga.create_next_generation()
        fitness = ga.best_individual()[0]
        y_axis_0.append(float(fitness))
        y_axis_1.append(float(get_average_fitness(ga)))
        x_axis_0.append(float(format(i)))

    elapsed_time = time() - start_time

    print("")
    print("board solved")
    print(f"selection method used: {parents_selection_option}")
    print("execution time: %0.2f seconds" % elapsed_time)
    print(f"errors: {ga.best_individual()[0]}")
    print(f"elapsed generations: {generations}")
    print(f"population: {population}")

    save_board(
        ga.best_individual()[1],
        path.join(results_path_boards, f"{board_name}_ga_result.txt"),
    )

    custom_fitness_report(ga.best_individual()[1])
    print("saving algorithm performance trace")

    plt.figure(figsize=(16, 9))

    plt.plot(
        x_axis_0,
        y_axis_1,
        "-",
        linewidth=0.4,
        color="b",
        label=f"average fitness trace [population: {population}]",
    )

    plt.plot(
        x_axis_0,
        y_axis_0,
        "-",
        linewidth=0.8,
        color="r",
        label=f"best fitness trace [errors: {ga.best_individual()[0]}]",
    )

    plt.xlabel("generation")
    plt.ylabel("fitness")
    plt.legend()
    plt.grid()
    plt.savefig(path.join(results_path_images, f"{board_name}_ga_performance.png"))
    plt.clf()

    del board_a, board_b
    print("algorithm performance trace saved")
    print("")
