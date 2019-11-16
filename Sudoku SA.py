import numpy as np
import random as rn
from time import time
from copy import deepcopy
import matplotlib.pyplot as plt
from operator import itemgetter


def annealing(estado_inicial, funcion_costo, siguiente_estado, acceptance_probability, generar_reporte, temp_inicial,
              temp_decrease_factor, maxsteps):
    solutions = []
    T = temp_inicial

    while T > 0.01:
        state = estado_inicial()
        cost = funcion_costo(state)
        for step in range(maxsteps):
            new_state = siguiente_estado(state)
            if acceptance_probability(cost, funcion_costo(new_state), T) > rn.random():
                solutions.append((funcion_costo(new_state), new_state))
        T *= temp_decrease_factor

    solutionsc = deepcopy(solutions)
    solutions = sorted(solutions, key=itemgetter(0))

    print("\nMejor costo:", solutions[0][0], "\nMejor solucion:\n")
    imprimirsudoku(solutions[0][1])
    print("\nErrores totales: ", funcion_costo(solutions[0][1]))
    generar_reporte(solutions[0][1])
    return solutions, [int(solutionsc[i][0]) for i in range(len(solutionsc))]


def cost_function_report(individual):
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


def cost_function(individual):
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


def siguiente_estado(individual):
    individuali = deepcopy(individual)
    if1 = rn.randrange(len(individual))
    ic1 = rn.randrange(len(individual[if1]))
    ic2 = rn.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = individual[if1][ic2], individual[if1][ic1]
    individual = correct(individual, if1)
    if cost_function(individual) <= cost_function(individuali):
        return individual
    else:
        return individuali


def correct(individual, fi1):
    for col1 in range(len(TableroB[fi1])):
        if TableroB[fi1][col1] is not 0 and individual[fi1][col1] is not TableroB[fi1][col1]:
            col2 = individual[fi1].index(TableroB[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = individual[fi1][col2], individual[fi1][col1]
    return individual


def algoritmo_metropolis(cost, new_cost, temperature):
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temperature)
        return p


def imprimirsudoku(sudoku):
    for fila in sudoku:
        for numero in fila:
            print(numero, end=" ")
        print("")


def estado_inicial():
    return TableroA


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

for fila in TableroA:
    for indice in range(len(fila)):
        if fila[indice] is 0:
            while True:
                nuevonumero = rn.randrange(1, 10)
                if nuevonumero not in fila:
                    break
            fila[indice] = nuevonumero

start_time = time()
states, costs = annealing(
    estado_inicial,
    cost_function,
    siguiente_estado,
    algoritmo_metropolis,
    cost_function_report,
    temp_inicial=200,
    temp_decrease_factor=0.8,
    maxsteps=2000
)
elapsed_time = time() - start_time

print("\nTiempo de ejecucion: %0.10f segundos" % elapsed_time)

plt.plot(costs, '-', linewidth=0.8, color='r')
plt.xlabel('Solucion')
plt.ylabel('Costo')
plt.grid()
plt.show()
