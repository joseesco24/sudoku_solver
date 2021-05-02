import random
import itertools
from time import time
from copy import deepcopy
import matplotlib.pyplot as plt

# ------------- Parametros del tablero:
ruta_tablero = "TableroD2.txt"  # ruta al tablero que se quiere resolver.
tamano_zona = (
    3,
    2,
)  # tamaño de las zonas individuales, respectivamente columnas, filas.

# ------------- Parametros Hill Climbing:
numero_reinicios = 4  # numero de veces que se reinicia el tablero en random restart, solo afecta si la configuracion es 3.
numero_de_busquedas = 400  # numero de veces que se generaran estados y se buscara el mejor segin el criterio.
configuracion_HC = 3  # <---- 0, 1, 2 o 3, steep, stochastic, first-choice o random restart, este es el criterio de busqueda del mejor.


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
def fitness(individual):
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
# Funcion de correccion de filas, se usa luego de cada mutacion o cruce para corregir la fila en caso de
# al mutar o cruzar los numeros fijos hayan sido movios de su posicion original, para esto se usa el
# TableroB, que es una copia del TableroA antes de ser inciado.
# --------------------------------------------------------------------------------------------------------
def corregir_fila(individual, fi1):
    for col1 in range(len(TableroB[fi1])):
        if TableroB[fi1][col1] != 0 and individual[fi1][col1] != TableroB[fi1][col1]:
            col2 = individual[fi1].index(TableroB[fi1][col1])
            individual[fi1][col1], individual[fi1][col2] = (
                individual[fi1][col2],
                individual[fi1][col1],
            )
    return individual


# --------------------------------------------------------------------------------------------------------
# Genera todos los posibles estados del tablero variando solo una fila seleccionado al asar en el metodo
# mejorar_n.
# --------------------------------------------------------------------------------------------------------
def generar_estados(individual, fila):
    if1 = fila
    estados = []
    numeros_moviles = list(
        filter(
            lambda x: x not in TableroB[if1],
            [n for n in range(1, (tamano_zona[0] * tamano_zona[-1]) + 1)],
        )
    )
    variaciones_numeros_moviles = list(
        itertools.permutations(numeros_moviles, len(numeros_moviles))
    )
    for variacion_fila in variaciones_numeros_moviles:
        Fila = [n for n in TableroB[if1]]
        variacion_fila = list(variacion_fila)
        for i in range(len(TableroB[if1])):
            if Fila[i] == 0:
                Fila[i] = variacion_fila[0]
                variacion_fila.remove(variacion_fila[0])
        estados.append((fitness(individual), Fila))
    return estados


# --------------------------------------------------------------------------------------------------------
# Esto realmente es una mutacion, es bastante simple, se toma una fila al asar, de la fila se seleccionan
# dos posiciones tambien al asar y se intercambian, luego se aplica la funcion de correccion al individo
# en la fila seleccionada, asi se asegura que no se muevan los numeros fijos, tambien hay un condicional
# que evita que el individuo pueda mutar a un tablero con un fitness mejor al inicial.
# --------------------------------------------------------------------------------------------------------
def mejorar_1(individual):
    individuali = deepcopy(individual)
    if1 = random.randrange(len(individual))
    ic1 = random.randrange(len(individual[if1]))
    ic2 = random.randrange(len(individual[if1]))
    individual[if1][ic1], individual[if1][ic2] = (
        individual[if1][ic2],
        individual[if1][ic1],
    )
    individual = corregir_fila(individual, if1)
    if fitness(individual) <= fitness(individuali):
        return individual
    else:
        return individuali


# --------------------------------------------------------------------------------------------------------
# Es probablemente el peor criterio que hay, genera todas las posibles variaciones de una fila y incorpora
# una de las variaciones finales a la solucion, la seleccion de la fila que se incorporara es al asar.
# --------------------------------------------------------------------------------------------------------
def mejorar_2(individual):
    fila_a_mejorar = random.randrange(len(individual))
    estados = generar_estados(individual, fila_a_mejorar)
    nueva_fila = random.choice(estados)
    individual[fila_a_mejorar] = nueva_fila[-1]
    return individual


# --------------------------------------------------------------------------------------------------------
# Es practicamente igual que el hill climbien normal en terminos de desempeño, pero deberia ser mas
# costoso computacionalmente hablando, la ventaja es que es mas rapido, pero es mas propenso a caer en
# minimos locales que la mutacion del hill climbing normal.
# --------------------------------------------------------------------------------------------------------
def mejorar_3(individual):
    individuali = deepcopy(individual)
    fila_a_mejorar = random.randrange(len(individual))
    estados = generar_estados(individual, fila_a_mejorar)
    nueva_fila = random.choice(estados)
    individual[fila_a_mejorar] = nueva_fila[-1]
    if fitness(individual) < fitness(individuali):
        return individual
    else:
        return individuali


# --------------------------------------------------------------------------------------------------------
# Ciclo de mejora, dependiendo del criterio de busqueda.
# --------------------------------------------------------------------------------------------------------
def mejorar_n(individual, n):
    puntuaciones = []
    tableros = []

    if configuracion_HC == 0:
        for i in range(n + 1):
            individual = mejorar_1(individual)
            puntuaciones.append(fitness(individual))
        return individual, puntuaciones

    if configuracion_HC == 1:
        for i in range(n + 1):
            individual = mejorar_2(individual)
            tableros.append(deepcopy(individual))
            puntuaciones.append(fitness(individual))
        for i in tableros:
            if fitness(i) < fitness(individual):
                individual = i
        return individual, puntuaciones

    if configuracion_HC == 2:
        for i in range(n + 1):
            individual = mejorar_3(individual)
            puntuaciones.append(fitness(individual))
        return individual, puntuaciones

    if configuracion_HC == 3:
        for i in range(numero_reinicios + 1):
            individual = iniciar_tablero(leer_tablero_incial(ruta_tablero))
            for i in range(n + 1):
                individual = mejorar_1(individual)
                tableros.append(individual)
                puntuaciones.append(fitness(individual))
        for i in tableros:
            if fitness(i) < fitness(individual):
                individual = i
        return individual, puntuaciones


# --------------------------------------------------------------------------------------------------------
# Imprime el tablero.
# --------------------------------------------------------------------------------------------------------
def imprimirsudoku(sudoku):
    for fila in sudoku:
        for numero in fila:
            print(numero, end=" ")
        print("")


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
# Inicia el tablero, llena las posiciones de las filas iniciadas como 0 con numeros al asar que no esten
# presentes en la fila, asi desde el principio se evitan las colisions en las filas.
# --------------------------------------------------------------------------------------------------------
def iniciar_tablero(TableroA):
    for fila in TableroA:
        for indice in range(len(fila)):
            if fila[indice] == 0:
                while True:
                    nuevonumero = random.randrange(
                        1, (tamano_zona[0] * tamano_zona[-1]) + 1
                    )
                    if nuevonumero not in fila:
                        break
                fila[indice] = nuevonumero
    return TableroA


# --------------------------------------------------------------------------------------------------------
# Ejecucion del programa.
# --------------------------------------------------------------------------------------------------------
TableroA = leer_tablero_incial(ruta_tablero)
TableroB = deepcopy(TableroA)
TableroA = iniciar_tablero(TableroA)

start_time = time()
TableroA, puntuaciones = mejorar_n(TableroA, numero_de_busquedas)
elapsed_time = time() - start_time

print("\nTiempo de ejecucion: %0.10f segundos" % elapsed_time)
print("Numero de errores mejor solucion: " + str(fitness(TableroA)) + "\n")
imprimirsudoku(TableroA)
print("")
fitness_report(TableroA)
print("")

plt.figure(figsize=(16, 9))
plt.plot(puntuaciones, "-", linewidth=0.8, color="r")
plt.xlabel("Iteracion")
plt.ylabel("Numero de errores")
plt.grid()
plt.show()
plt.savefig("./imagenes/hc_performance.png")
