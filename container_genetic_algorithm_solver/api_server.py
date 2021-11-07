from general_solver_functions_access import calculate_board_fitness_report

from genetic_algorithm import solve_using_genetic_algorithm

from aiohttp.web_request import Request
from http import HTTPStatus
from aiohttp import web
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()


@api_routes.get(r"/health_test")
async def health_test(_: Request) -> web.Response:

    """Health Test

    This function is incharge of response all the health check petitions that the middle proxy makes for checking if the requested
    solver is active before making a solver request.

    Returns:
        web.Response: A 200 status code.
    """

    return web.Response(
        status=HTTPStatus.OK,
    )


@api_routes.get(r"/solver")
async def solver(request: Request) -> web.Response:

    """Solver

    This function is in charge to expose the solver functionality, this function receives the board solve parameters and initial
    board in the body of a json http request and returns response with the board best solution that this solver could find using a
    genetic algorithm in the response body also using json format.

    Args:
        request (aiohttp.web_request.Request): An http request verified for the middle proxy that contains in the body the solve
        parameters and the initial board.

    Returns:
        web.Response: A 200 status code and a json body with the board solution if everything goes right, 500 if something goes
        wrong with an error message or a 401 code if the api key used by the middle proxy is wrong for some reason.
    """

    try:

        request_header_keys = [key for key in request.headers.keys()]

        if (
            "Authorization" in request_header_keys
            and request.headers["Authorization"] == os.environ["ACCESS_KEY"]
        ):

            generations_validator, population_validator = True, True
            mutation_validator, crossover_validator = True, True

            generations, population = 10, 10
            mutation, crossover = 0.2, 0.8

            request_body = await request.json()

            sudoku_initial_board = request_body["board_array"]
            sudoku_zone_height = request_body["zone_height"]
            sudoku_zone_length = request_body["zone_length"]

            request_body_keys = [key for key in request_body.keys()]

            # Validation and search of specific solver parameters.

            if "generations" in request_body_keys:

                if not type(request_body["generations"]) is int:
                    generations_validator = False

                if not request_body["generations"] > 0:
                    generations_validator = False

                if generations_validator is True:
                    generations = request_body["generations"]

            if "population" in request_body_keys:

                if not type(request_body["population"]) is int:
                    population_validator = False

                if not request_body["population"] > 0:
                    population_validator = False

                if population_validator is True:
                    population = request_body["population"]

            if "mutation" in request_body_keys:

                if not type(request_body["mutation"]) is float:
                    mutation_validator = False

                if not 0 < request_body["mutation"] <= 1:
                    mutation_validator = False

                if mutation_validator is True:
                    mutation = request_body["mutation"]

            if "crossover" in request_body_keys:

                if not type(request_body["crossover"]) is float:

                    crossover_validator = False
                if not 0 < request_body["crossover"] <= 1:
                    crossover_validator = False

                if crossover_validator is True:
                    crossover = request_body["crossover"]

            solution_board = await solve_using_genetic_algorithm(
                genetic_algorithm_generations=generations,
                genetic_algorithm_population=population,
                genetic_algorithm_crossover=crossover,
                genetic_algorithm_mutation=mutation,
                zone_height=sudoku_zone_height,
                zone_length=sudoku_zone_length,
                board=sudoku_initial_board,
            )

            (
                total_collisions,
                column_collisions,
                row_collisions,
                zone_collisions,
            ) = await calculate_board_fitness_report(
                zone_height=sudoku_zone_height,
                zone_length=sudoku_zone_length,
                board=solution_board,
            )

            response_dict = {
                "total collisions": total_collisions,
                "column collisions": column_collisions,
                "row collisions": row_collisions,
                "zone collisions": zone_collisions,
                "board array": solution_board,
            }

            return web.Response(
                body=json.dumps(obj=response_dict, indent=None),
                status=HTTPStatus.OK,
            )

        else:
            return web.Response(
                reason=r"you aren't authorized to use this api",
                status=HTTPStatus.UNAUTHORIZED,
            )

    except:

        return web.Response(
            reason=r"internal error inside the solver server",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["ACCESS_PORT"]))
