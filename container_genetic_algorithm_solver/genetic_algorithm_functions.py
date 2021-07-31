from copy import deepcopy
import itertools
import random
import math


async def roulette_selection(population: list) -> tuple:

    """Roulette Selection

    This function is used to select an individual from all the population based on it's fitness score for making the crossover.

    Args:
        population (list): The probability of the event occurrence.

    Returns:
        tuple: An individual chromosome representation for the crossover.
    """

    roulette = list()

    for individual in population:

        fitness_score = int(individual[0])

        if fitness_score == 0:
            probability = len(population)

        if fitness_score != 0:
            probability = int(math.ceil(len(population) / fitness_score))

        for _ in itertools.repeat(None, probability):
            roulette.append(individual)

    random.shuffle(roulette)

    return random.choice(roulette)


async def exchange_random_row(individual_1: list, individual_2: list) -> list:

    """Exchange Random Row

    This function is used for making the crossover between two individuals, in picks a random row an exchange it between the two
    given individuals.

    Args:
        individual_1 (list): The representation of the first individual.
        individual_2 (list): The representation of the second individual.

    Returns:
        tuple: one of the individuals after making the rows exchange.
    """

    exchange_index = random.randrange(len(individual_1))

    individual_1[exchange_index], individual_2[exchange_index] = (
        deepcopy(individual_2[exchange_index]),
        deepcopy(individual_1[exchange_index]),
    )

    return random.choice([individual_1, individual_2])
