import random
from time import time
from copy import deepcopy
from pyeasyga import pyeasyga
import matplotlib.pyplot as plt
from operator import attrgetter


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
    for fila in range(0, len(individual), 3):
        for columna in range(0, len(individual[fila]), 3):
            sub1 = individual[columna + 0][fila:fila + 3]
            sub2 = individual[columna + 1][fila:fila + 3]
            sub3 = individual[columna + 2][fila:fila + 3]
            sub = set(sub1 + sub2 + sub3)
            repeticiones = abs(len(individual[fila]) - len(sub))
            colisioneszon += repeticiones
    print("Errores en las zonas: " + str(colisioneszon))
    print("Errores en las filas: " + str(colisionesfil))
    print("Errores en las columnas: " + str(colisionescol))


def fitness(individual, data):
    colisiones = 0
    for fila in range(len(individual)):
        numeros = set()
        for columna in range(len(individual[fila])):
            numeros.add(individual[columna][fila])
        repeticiones = abs(len(individual[fila]) - len(numeros))
        colisiones += repeticiones
    for fila in range(0, len(individual), 3):
        for columna in range(0, len(individual[fila]), 3):
            sub1 = individual[columna + 0][fila:fila + 3]
            sub2 = individual[columna + 1][fila:fila + 3]
            sub3 = individual[columna + 2][fila:fila + 3]
            sub = set(sub1 + sub2 + sub3)
            repeticiones = abs(len(individual[fila]) - len(sub))
            colisiones += repeticiones
    return colisiones


def create_individual(data):
    for fila in data:
        for indice in range(len(fila)):
            if fila[indice] is 0:
                while True:
                    nuevonumero = random.randrange(1, 10)
                    if nuevonumero not in fila:
                        break
                fila[indice] = nuevonumero
    return data


def selection(population):
    tournmentsize = len(population) // 2
    if tournmentsize is 0:
        tournmentsize = 2
    members = random.sample(population, tournmentsize)
    members.sort(key=attrgetter('fitness'), reverse=False)
    return members[0]


def correct(individual, fi1):
    for col1 in range(len(TableroB[fi1])):
        if TableroB[fi1][col1] is not 0 and individual[fi1][col1] is not TableroB[fi1][col1]:
            col2 = individual[fi1].index(TableroB[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = individual[fi1][col2], individual[fi1][col1]
    return individual


def mutate(individual):
    if1 = random.randrange(len(individual))
    ic1 = random.randrange(len(individual[if1]))
    ic2 = random.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = individual[if1][ic2], individual[if1][ic1]
    return correct(individual, if1)


def imprimirsudoku(sudoku):
    for fila in sudoku:
        for numero in fila:
            print(numero, end=" ")
        print("")


def crossover(parent_1, parent_2):
    if1 = random.randrange(len(parent_1))
    if2 = random.randrange(len(parent_1))
    parent_1[if1], parent_2[if2] = parent_2[if2], parent_1[if1]
    return correct(parent_1, if1), correct(parent_2, if2)


def average_fitness():
    fitness_po = [i.fitness for i in ga.current_generation]
    average = sum(fitness_po) / len(fitness_po)
    return format(average)


TableroA = []
archivo = open('TableroD1.txt', 'r')
lineas = list(archivo)
for linea in lineas:
    linea = linea.split(" ")
    linea = [x for x in filter(lambda x: x is not "\n", linea)]
    for i in range(len(linea)):
        linea[i] = int(linea[i])
    TableroA.append(linea)
archivo.close()

TableroB = deepcopy(TableroA)

ga = pyeasyga.GeneticAlgorithm(
    TableroA,
    population_size=200,
    crossover_probability=0.8,
    mutation_probability=0.2,
    elitism=False,
    maximise_fitness=False
)

ga.create_individual = create_individual
ga.crossover_function = crossover
ga.mutate_function = mutate
ga.selection_function = selection
ga.fitness_function = fitness
ga.create_first_generation()

ejey0 = []
ejey1 = []
ejex0 = []

start_time = time()
it = 0
for i in range(400 + 1):
    it = i
    ga.create_next_generation()
    fitness = ga.best_individual()[0]
    ejey0.append(float(fitness))
    ejey1.append(float(average_fitness()))
    ejex0.append(float(format(i)))
elapsed_time = time() - start_time

print("\nTiempo de ejecucion: %0.10f segundos" % elapsed_time)
print("Numero de errores mejor solucion: " + str(ga.best_individual()[0]))
print("Numero de la generacion: " + str(it) + "\n")
imprimirsudoku(ga.best_individual()[1])
print("")
fitness_report(ga.best_individual()[1])

plt.plot(ejex0, ejey1, '-', linewidth=0.4, color='b', label='Traza fitness promedio')
plt.plot(ejex0, ejey0, '-', linewidth=0.8, color='r', label='Traza mejor fitness')
plt.xlabel('Generacion')
plt.ylabel('Fitness')
plt.grid()
plt.show()
