import random
from time import time
from copy import deepcopy
import matplotlib.pyplot as plt


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


def fitness(individual):
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


def mejorar1(individual):
    individuali = deepcopy(individual)
    if1 = random.randrange(len(individual))
    ic1 = random.randrange(len(individual[if1]))
    ic2 = random.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = individual[if1][ic2], individual[if1][ic1]
    individual = correct(individual, if1)
    if fitness(individual) <= fitness(individuali):
        return individual
    else:
        return individuali


def mejorarn(individual, n):
    puntuaciones = []
    for i in range(n + 1):
        individual = mejorar1(individual)
        puntuaciones.append(fitness(individual))
    return individual, puntuaciones


def correct(individual, fi1):
    for col1 in range(len(TableroB[fi1])):
        if TableroB[fi1][col1] is not 0 and individual[fi1][col1] is not TableroB[fi1][col1]:
            col2 = individual[fi1].index(TableroB[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = individual[fi1][col2], individual[fi1][col1]
    return individual


def imprimirsudoku(sudoku):
    for fila in sudoku:
        for numero in fila:
            print(numero, end=" ")
        print("")


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
                nuevonumero = random.randrange(1, 10)
                if nuevonumero not in fila:
                    break
            fila[indice] = nuevonumero

start_time = time()
TableroA, puntuaciones = mejorarn(TableroA, 40000)
elapsed_time = time() - start_time

print("\nTiempo de ejecucion: %0.10f segundos" % elapsed_time)
print("Numero de errores mejor solucion: " + str(fitness(TableroA)) + "\n")
imprimirsudoku(TableroA)
print("")
fitness_report(TableroA)

plt.plot(puntuaciones, '-', linewidth=0.8, color='r')
plt.xlabel('Solucion')
plt.ylabel('Costo')
plt.grid()
plt.show()
