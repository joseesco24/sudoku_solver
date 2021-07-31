from general_solver_functions_access_custom import calculate_board_fitness_single

from general_solver_functions_access import board_random_initialization
from general_solver_functions_access import board_random_mutation

from general_utilities import normalize_decimal
from general_utilities import print_log

from asyncio import gather
from copy import deepcopy
from time import time
import itertools
import random

script_firm = "gas"


async def random_decision(probability: float) -> bool:

    """Random Decision

    This function is used to decide if a random event based on a probability should or not occur.

    Args:
        probability (float): The probability of the event occurrence.

    Returns:
        bool: Indicates if the random event based on the probability should or not occur.
    """

    occurrence = random.uniform(0, 1)

    if occurrence > probability:
        return False

    else:
        return True


async def mutate(
    filled_board: list, fixed_numbers_board: list, mutation_probability: float
) -> list:

    """Mutate

    This function create a new board mutating the original board based on its mutation probability.

    Args:
        filled_board (list): A full filled board representation.
        fixed_numbers_board (list): A board representation that includes just the fixed numbers.
        mutation_probability (float): The mutation probability of the individual.

    Returns:
        list: The mutated board or a None if the board dosn't mutate.
    """

    occurrence = await random_decision(probability=mutation_probability)

    if occurrence is True:

        return await board_random_mutation(
            board=filled_board, fixed_numbers_board=fixed_numbers_board
        )

    else:

        return None


async def solve_using_genetic_algorithm(
    genetic_algorithm_crossover: float,
    genetic_algorithm_generations: int,
    genetic_algorithm_population: int,
    genetic_algorithm_mutation: float,
    zone_height: int,
    zone_length: int,
    board: list,
) -> list:

    fixed_numbers_board = deepcopy(board)

    print_log(r"starting to solve with genetic algorithm", script_firm)

    generations_counter = 0
    start_time = time()

    print_log(r"creating first generation", script_firm)

    population = await gather(
        *[
            board_random_initialization(
                fixed_numbers_board=fixed_numbers_board,
                zone_height=zone_height,
                zone_length=zone_length,
            )
            for _ in itertools.repeat(None, genetic_algorithm_population)
        ]
    )

    print_log(r"ranking first generation", script_firm)

    population = await gather(
        *[
            calculate_board_fitness_single(
                board=individual, zone_height=zone_height, zone_length=zone_length
            )
            for individual in population
        ]
    )

    print_log(r"starting to evolve population", script_firm)

    for _ in itertools.repeat(None, genetic_algorithm_generations):

        # Creating mutated population.

        mutated_population = await gather(
            *[
                mutate(
                    mutation_probability=genetic_algorithm_mutation,
                    fixed_numbers_board=fixed_numbers_board,
                    filled_board=individual[1],
                )
                for individual in population
            ]
        )

        # Filtering the mutated population.

        mutated_population = [
            mutation
            for mutation in filter(
                lambda mutated_individual: mutated_individual is not None,
                mutated_population,
            )
        ]

        # Ranking the mutated population.

        mutated_population = await gather(
            *[
                calculate_board_fitness_single(
                    zone_height=zone_height,
                    zone_length=zone_length,
                    board=individual,
                )
                for individual in mutated_population
            ]
        )

        # Extending and sorting population by individuals rank.

        population.extend(mutated_population)

        population = sorted(population, key=lambda individual: individual[0])

        # Removing the not apt individuals.

        population = population[:genetic_algorithm_population]

        # Increasing generations counter.

        generations_counter += 1

    end_time = time()
    elapsed_time = end_time - start_time

    print_log(r"finishing to solve with genetic algorithm", script_firm)

    print_log(f"total generations: {generations_counter}", script_firm)
    print_log(f"total population: {len(population)}", script_firm)

    print_log(
        f"time spent searching a solution: {normalize_decimal(elapsed_time)}s",
        script_firm,
    )

    return population[0][1]
