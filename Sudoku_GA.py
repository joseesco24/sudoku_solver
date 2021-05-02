import random
from time import time
from copy import deepcopy
from pyeasyga import pyeasyga
import matplotlib.pyplot as plt
from operator import attrgetter

# ------------- Nota:
# antes hay que instalar pyeasyga y matplotlib.
# pip install pyeasyga
# pip install matplotlib

# ------------- Parametros del tablero:
ruta_tablero = "TableroD2.txt"  # ruta al tablero que se quiere resolver.
tamano_zona = (
    3,
    2,
)  # tamaño de las zonas individuales, respectivamente columnas, filas.

# ------------- Parametros con los que no se puede jugar:
maximisar_fitness = False

# ------------- Parametros con los que se puede jugar:
numero_de_generaciones = 100
tamano_poblacion = 100
probablilidad_de_cruce = 0.8
probabilidad_de_mutacion = 0.2
elitimso = True
metodo_seleccion_padres = 1  # <---- 0, 1 o 2, torneo, ruleta o aleatorio.


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
def create_individual(data):
    for fila in data:
        for indice in range(len(fila)):
            if fila[indice] == 0:
                while True:
                    nuevonumero = random.randrange(
                        1, (tamano_zona[0] * tamano_zona[-1]) + 1
                    )
                    if nuevonumero not in fila:
                        break
                fila[indice] = nuevonumero
    return data


# --------------------------------------------------------------------------------------------------------
# Metodo de seleccion por torneo, es el mas simple, pero el mejor, toma a la mitad de los individuos de la
# la poblacion al asar y selecciona al mejor de los individuos presente en la mustra.
# --------------------------------------------------------------------------------------------------------
def torneo(population):
    tournmentsize = len(population) // 2
    if tournmentsize == 0:
        tournmentsize = 2
    members = random.sample(population, tournmentsize)
    members.sort(key=attrgetter("fitness"), reverse=False)
    return members[0]


# --------------------------------------------------------------------------------------------------------
# Metodo de seleccion de ruleta, reduce exponencialmente la probabilida de un individo entre mayor sea su
# fitness, dependiendo de su probabilidad el individo se pone cierto numero de veces en la ruleta, de esta
# forma entre menor el fitness mas apariciones del individuo en la ruleta y mas probabilidades de ser
# seleccionado, este es el metodo de seleccion mas lento, al usarlo la ejecucion puede tomar mucho mas
# tiempo que por torneo o aleatorio, lo mejor es usarlo con elitismo y una poblacion reducida.
# --------------------------------------------------------------------------------------------------------
def ruleta(population):
    ruleta = []
    for dude in population:
        fitnes = int(dude.fitness)
        if fitnes == 0:
            prob = 100
        if fitnes != 0:
            prob = int(100 / fitnes)
        for n in range(prob + 1):
            ruleta.append(dude)
    return random.choice(ruleta)


# --------------------------------------------------------------------------------------------------------
# Metodo de seleccion aleatorio, toma un individuo cualquiera de la poblacion para realizar los cruces.
# --------------------------------------------------------------------------------------------------------
def aleatorio(population):
    return random.choice(population)


metodos_seleccion = [torneo, ruleta, aleatorio]  # Vector de metodos de seleccion.


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
# Funcion de cruce, toma dos filas aleatorias de los padres y las intercambia, luego las corrige con la
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
# Lee el tablero inicial de un archivo .txt especificado como ruta_tablero.
# --------------------------------------------------------------------------------------------------------
def leer_tablero_incial(ruta_tablero):
    TableroA = []
    archivo = open(ruta_tablero, "r")
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
TableroA = leer_tablero_incial(ruta_tablero)
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
    maximise_fitness=maximisar_fitness,
)

# --------------------------------------------------------------------------------------------------------
# Se sobreescriven los metodos de mutacion, curce, creacion de individuo, seleccion, fitness y finalmente
# se inicia la primera generacion.
# --------------------------------------------------------------------------------------------------------
ga.create_individual = create_individual
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

print("\nTiempo de ejecucion: %0.10f segundos" % elapsed_time)
print("Numero de errores mejor solucion: " + str(ga.best_individual()[0]))
print("Numero de la generacion: " + str(it) + "\n")
imprimirsudoku(ga.best_individual()[1])
print("")
fitness_report(ga.best_individual()[1])

plt.plot(ejex0, ejey1, "-", linewidth=0.4, color="b", label="Traza fitness promedio")
plt.plot(ejex0, ejey0, "-", linewidth=0.8, color="r", label="Traza mejor fitness")
plt.xlabel("Generacion")
plt.ylabel("Fitness")
plt.legend()
plt.grid()
plt.savefig('./imagenes/ga_performance.png')
