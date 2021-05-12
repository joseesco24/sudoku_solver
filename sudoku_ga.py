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
import gc

directory_path = os.getcwd()

boards_path = path.join(directory_path, "boards")
results_path = path.join(directory_path, "results")

zone_dimensions = (3, 3)

generations = 40
population = 40
crossover_probability = 0.8
mutation_probability = 0.2
elitism_setup = True
metodo_seleccion_padres = 1

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    for argument_index in range(len(arguments)):
        if argument_index < (len(arguments) - 1):
            argument_value = arguments[argument_index]
            if argument_value == "--generations":
                generations = int(arguments[argument_index + 1])
            if argument_value == "--population":
                population = int(arguments[argument_index + 1])


def get_file_name(board_path):
    return path.basename(board_path).split(".")[0]


def fitness_report(individual):
    colisionesfil, colisionescol, colisioneszon = 0, 0, 0
    for fila in range(len(individual)):
        numeros = set()
        for columna in range(len(individual[fila])):
            numeros.add(individual[fila][columna])
        repeticiones = abs(len(individual[fila]) - len(numeros))
        colisionesfil += repeticiones
    for fila in range(len(individual)):
        numeros = set()
        for columna in range(len(individual[fila])):
            numeros.add(individual[columna][fila])
        repeticiones = abs(len(individual[fila]) - len(numeros))
        colisionescol += repeticiones
    for fila in range(0, len(individual), zone_dimensions[-1]):
        for columna in range(0, len(individual[fila]), zone_dimensions[0]):
            sub = set()
            for i in range(zone_dimensions[-1]):
                sub1 = individual[fila + i][columna : columna + zone_dimensions[0]]
                sub.update(set(sub1))
            repeticiones = abs((zone_dimensions[0] * zone_dimensions[-1]) - len(sub))
            colisioneszon += repeticiones
    print("errors in zones: " + str(colisioneszon))
    print("errors in rows: " + str(colisionesfil))
    print("erros in columns: " + str(colisionescol))


def fitness(individual, _):
    colisiones = 0
    for fila in range(len(individual)):
        numeros = set()
        for columna in range(len(individual[fila])):
            numeros.add(individual[columna][fila])
        repeticiones = abs(len(individual[fila]) - len(numeros))
        colisiones += repeticiones
    for fila in range(0, len(individual), zone_dimensions[-1]):
        for columna in range(0, len(individual[fila]), zone_dimensions[0]):
            sub = set()
            for i in range(zone_dimensions[-1]):
                sub1 = individual[fila + i][columna : columna + zone_dimensions[0]]
                sub.update(set(sub1))
            repeticiones = abs((zone_dimensions[0] * zone_dimensions[-1]) - len(sub))
            colisiones += repeticiones
    return colisiones


def create(data):
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


def correct(individual, fi1):
    for col1 in range(len(board_b[fi1])):
        if board_b[fi1][col1] != 0 and individual[fi1][col1] != board_b[fi1][col1]:
            col2 = individual[fi1].index(board_b[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = (
                individual[fi1][col2],
                individual[fi1][col1],
            )
    return individual


def mutate(individual):
    if1 = random.randrange(len(individual))
    ic1 = random.randrange(len(individual[if1]))
    ic2 = random.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = (
        individual[if1][ic2],
        individual[if1][ic1],
    )
    return correct(individual, if1)


def imprimirsudoku(sudoku):
    for fila in sudoku:
        for numero in fila:
            print(numero, end=" ")


def crossover(parent_1, parent_2):
    if1 = random.randrange(len(parent_1))
    if2 = random.randrange(len(parent_1))
    parent_1[if1], parent_2[if2] = parent_2[if2], parent_1[if1]
    return correct(parent_1, if1), correct(parent_2, if2)


def average_fitness():
    fitness_po = [i.fitness for i in ga.current_generation]
    average = sum(fitness_po) / len(fitness_po)
    return format(average)


def leer_tablero_incial(board_path):
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

for file_name in txt_files_list:

    board_path = path.join(boards_path, file_name)
    board_a = leer_tablero_incial(board_path)
    board_b = deepcopy(board_a)

    ejey0 = list()
    ejey1 = list()
    ejex0 = list()

    start_time = time()
    generations_counter = 0

    print(f"board name: {get_file_name(board_path)}")
    print(f"board path: {board_path}")

    ga = pyeasyga.GeneticAlgorithm(
        seed_data=board_a,
        population_size=population,
        crossover_probability=crossover_probability,
        mutation_probability=mutation_probability,
        elitism=elitism_setup,
        maximise_fitness=False,
    )

    ga.create_individual = create
    ga.crossover_function = crossover
    ga.mutate_function = mutate
    ga.selection_function = [
        tournament_selection,
        roulette_selection,
        random_selection,
    ][metodo_seleccion_padres]
    ga.fitness_function = fitness
    ga.create_first_generation()

    print("starting to solve the board")

    for i in range(generations + 1):
        generations_counter = i
        ga.create_next_generation()
        fitness = ga.best_individual()[0]
        ejey0.append(float(fitness))
        ejey1.append(float(average_fitness()))
        ejex0.append(float(format(i)))
    elapsed_time = time() - start_time

    print("board solved")
    print(f"selection method used: {metodo_seleccion_padres}")
    print("execution time: %0.2f seconds" % elapsed_time)
    print(f"errors: {ga.best_individual()[0]}")
    print(f"generations: {generations_counter}")
    print(f"population: {population}")

    # imprimirsudoku(ga.best_individual()[1])

    fitness_report(ga.best_individual()[1])

    plt.figure(figsize=(16, 9))
    plt.plot(ejex0, ejey1, "-", linewidth=0.4, color="b", label="average fitness trace")
    plt.plot(ejex0, ejey0, "-", linewidth=0.8, color="r", label="best fitness trace")
    plt.xlabel("generation")
    plt.ylabel("fitness")
    plt.legend()
    plt.grid()
    plt.savefig("./results/ga_performance.png")

    del ga, board_a, board_b
    gc.collect()
