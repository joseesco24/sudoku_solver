import matplotlib.pyplot as plt
from operator import attrgetter
from pyeasyga import pyeasyga
from copy import deepcopy
from time import time
from os import path
import random
import sys
import os

script_path = path.realpath(__file__)
directory_path = os.getcwd()

#board_path = path.join(directory_path, "boards")
board_path = "./boards/tablero_d2.txt"
images_path = path.join(directory_path, "images")

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    for argument_index in range(len(arguments)):

        argument_value = arguments[argument_index]

        if argument_value == "--path" or argument_value == "-p":
            board_path = arguments[argument_index + 1]

tamano_zona = (3, 2)

numero_de_generaciones = 60
tamano_poblacion = 40
probablilidad_de_cruce = 0.8
probabilidad_de_mutacion = 0.2
elitimso = True
metodo_seleccion_padres = (
    1  # 0, 1 o 2, tournament_selection, ruleta o random_selection.
)


def get_file_name(board_path):
    return path.basename(board_path).split(".")[0]


# --------------------------------------------------------------------------------------------------------
# Funcion de reporte de fitness, calcula las colisiones en las filas, las columnas las zonas y las imprime.
# Solo de usa al final del programa para comprobar los resultados e imprimirlos
# --------------------------------------------------------------------------------------------------------
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
    for fila in range(0, len(individual), tamano_zona[-1]):
        for columna in range(0, len(individual[fila]), tamano_zona[0]):
            sub = set()
            for i in range(tamano_zona[-1]):
                sub1 = individual[fila + i][columna : columna + tamano_zona[0]]
                sub.update(set(sub1))
            repeticiones = abs((tamano_zona[0] * tamano_zona[-1]) - len(sub))
            colisioneszon += repeticiones
    print("Errores en las zonas: " + str(colisioneszon))
    print("Errores en las filas: " + str(colisionesfil))
    print("Errores en las columnas: " + str(colisionescol))


# --------------------------------------------------------------------------------------------------------
# Funcion de fitness, calcula las colisiones en las filas, las columnas y las zonas, esta funcion se usa
# Para calificar el desempeño de cada indivuo de la poblacion.
# --------------------------------------------------------------------------------------------------------
def fitness(individual, data):
    colisiones = 0
    for fila in range(len(individual)):
        numeros = set()
        for columna in range(len(individual[fila])):
            numeros.add(individual[columna][fila])
        repeticiones = abs(len(individual[fila]) - len(numeros))
        colisiones += repeticiones
    for fila in range(0, len(individual), tamano_zona[-1]):
        for columna in range(0, len(individual[fila]), tamano_zona[0]):
            sub = set()
            for i in range(tamano_zona[-1]):
                sub1 = individual[fila + i][columna : columna + tamano_zona[0]]
                sub.update(set(sub1))
            repeticiones = abs((tamano_zona[0] * tamano_zona[-1]) - len(sub))
            colisiones += repeticiones
    return colisiones


# --------------------------------------------------------------------------------------------------------
# Inicia individuo, llena las posiciones de las filas iniciadas como 0 con numeros al asar que no esten
# presentes en la fila, asi desde el principio se evitan las colisions en las filas, se usa solo para
# iniciar la primera generacion.
# --------------------------------------------------------------------------------------------------------
def create(data):
    for row in data:
        for index in range(len(row)):
            if row[index] == 0:
                while True:
                    new_number = random.randrange(
                        1, (tamano_zona[0] * tamano_zona[-1]) + 1
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


metodos_seleccion = [
    tournament_selection,
    roulette_selection,
    random_selection,
]


# --------------------------------------------------------------------------------------------------------
# Funcion de correccion de filas, se usa luego de cada mutacion o cruce para corregir la fila en caso de
# al mutar o cruzar los numeros fijos hayan sido movios de su posicion original, para esto se usa el
# TableroB, que es una copia del TableroA antes de ser inciado.
# --------------------------------------------------------------------------------------------------------
def correct(individual, fi1):
    for col1 in range(len(TableroB[fi1])):
        if TableroB[fi1][col1] != 0 and individual[fi1][col1] != TableroB[fi1][col1]:
            col2 = individual[fi1].index(TableroB[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = (
                individual[fi1][col2],
                individual[fi1][col1],
            )
    return individual


# --------------------------------------------------------------------------------------------------------
# Funcion de mutacion, es bastante simple, se toma una fila al asar, de la fila se seleccionan
# dos posiciones tambien al asar y se intercambian, luego se aplica la funcion de correccion al individo
# en la fila seleccionada, asi se asegura que no se muevan los numeros fijos, tambien hay un condicional
# que evita que el individuo pueda mutar a un tablero con un fitness mejor al inicial.
# --------------------------------------------------------------------------------------------------------
def mutate(individual):
    if1 = random.randrange(len(individual))
    ic1 = random.randrange(len(individual[if1]))
    ic2 = random.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = (
        individual[if1][ic2],
        individual[if1][ic1],
    )
    return correct(individual, if1)


# --------------------------------------------------------------------------------------------------------
# Imprime el tablero.
# --------------------------------------------------------------------------------------------------------
def imprimirsudoku(sudoku):
    for fila in sudoku:
        for numero in fila:
            print(numero, end=" ")
        print("")


# --------------------------------------------------------------------------------------------------------
# Funcion de cruce, toma dos filas aleatorias de los padres         for n in range(prob + 1):y las intercambia, luego las corrige con la
# funcion de correccion para evitar mover los numeros que deben permanecer fijos.
# --------------------------------------------------------------------------------------------------------
def crossover(parent_1, parent_2):
    if1 = random.randrange(len(parent_1))
    if2 = random.randrange(len(parent_1))
    parent_1[if1], parent_2[if2] = parent_2[if2], parent_1[if1]
    return correct(parent_1, if1), correct(parent_2, if2)


# --------------------------------------------------------------------------------------------------------
# Funcion que extrae el fitness promedio de cada generacion.
# --------------------------------------------------------------------------------------------------------
def average_fitness():
    fitness_po = [i.fitness for i in ga.current_generation]
    average = sum(fitness_po) / len(fitness_po)
    return format(average)


# --------------------------------------------------------------------------------------------------------
# Lee el tablero inicial de un archivo .txt especificado como board_path.
# --------------------------------------------------------------------------------------------------------
def leer_tablero_incial(board_path):
    TableroA = []
    archivo = open(board_path, "r")
    lineas = list(archivo)
    for linea in lineas:
        linea = linea.split(" ")
        linea = [x for x in filter(lambda x: x != "\n", linea)]
        for i in range(len(linea)):
            linea[i] = int(linea[i])
        TableroA.append(linea)
    archivo.close()
    return TableroA


# --------------------------------------------------------------------------------------------------------
# Ejecucion del programa.
# --------------------------------------------------------------------------------------------------------
TableroA = leer_tablero_incial(board_path)
TableroB = deepcopy(TableroA)

# --------------------------------------------------------------------------------------------------------
# Se definen los parametros del algoritmo genetico.
# --------------------------------------------------------------------------------------------------------
ga = pyeasyga.GeneticAlgorithm(
    TableroA,
    population_size=tamano_poblacion,
    crossover_probability=probablilidad_de_cruce,
    mutation_probability=probabilidad_de_mutacion,
    elitism=elitimso,
    maximise_fitness=False,
)

# --------------------------------------------------------------------------------------------------------
# Se sobreescriven los metodos de mutacion, curce, creacion de individuo, seleccion, fitness y finalmente
# se inicia la primera generacion.
# --------------------------------------------------------------------------------------------------------
ga.create_individual = create
ga.crossover_function = crossover
ga.mutate_function = mutate
ga.selection_function = metodos_seleccion[metodo_seleccion_padres]
ga.fitness_function = fitness
ga.create_first_generation()

ejey0 = []
ejey1 = []
ejex0 = []

# --------------------------------------------------------------------------------------------------------
# Se empieza a iterar a traves de las generaciones agregando los fitness mas altos y promedio a los ejes
# y1 y y0 y el numero de la generacion al eje x0.
# --------------------------------------------------------------------------------------------------------
start_time = time()
it = 0
for i in range(numero_de_generaciones + 1):
    it = i
    ga.create_next_generation()
    fitness = ga.best_individual()[0]
    ejey0.append(float(fitness))
    ejey1.append(float(average_fitness()))
    ejex0.append(float(format(i)))
elapsed_time = time() - start_time

print("")
print("Execution time: %0.10f seconds" % elapsed_time)
print(f"Board name: {str(get_file_name(board_path))}")
print(f"Errors: {str(ga.best_individual()[0])}")
print(f"Generations: {str(it)}")
print("")
imprimirsudoku(ga.best_individual()[1])
print("")
fitness_report(ga.best_individual()[1])
print("")

plt.figure(figsize=(16, 9))
plt.plot(ejex0, ejey1, "-", linewidth=0.4, color="b", label="Traza fitness promedio")
plt.plot(ejex0, ejey0, "-", linewidth=0.8, color="r", label="Traza mejor fitness")
plt.xlabel("Generacion")
plt.ylabel("Fitness")
plt.legend()
plt.grid()
plt.savefig("./images/ga_performance.png")
