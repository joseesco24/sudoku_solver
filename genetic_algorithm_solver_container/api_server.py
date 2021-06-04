from general_solver_functions_access import calculate_board_fitness_single

from genetic_algorithm import solve_using_genetic_algorithm

from general_utilities import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()

script_firm = "api"


@api_routes.get(r"/solver")
async def solver(request: Request):

    request_header_keys = [key for key in request.headers.keys()]

    if (
        "Authorization" in request_header_keys
        and request.headers["Authorization"] == os.environ["SELF_ACCESS_KEY"]
    ):

        restarts, searchs = 10, 10

        request_body = await request.json()
        request_body_keys = [key for key in request_body.keys()]

        sudoku_initial_board = request_body["board_array"]
        sudoku_zone_height = request_body["zone_height"]
        sudoku_zone_length = request_body["zone_length"]

        # Validation and search of specific solver parameters.

        if "restarts" in request_body_keys:
            if type(request_body["restarts"]) is int:
                print_log(
                    r"the variable restarts has the correct data type", script_firm
                )
                restarts = request_body["restarts"]
            else:
                print_log(
                    r"the variable restarts hasn't the correct data type, using default value",
                    script_firm,
                )
        if "searchs" in request_body_keys:
            if type(request_body["searchs"]) is int:
                print_log(
                    r"the variable searchs has the correct data type", script_firm
                )
                searchs = request_body["searchs"]
            else:
                print_log(
                    r"the variable searchs hasn't the correct data type, using default value",
                    script_firm,
                )

        solution_board = await solve_using_genetic_algorithm(
            hill_climbing_restarts=restarts,
            hill_climbing_searchs=searchs,
            zone_height=sudoku_zone_height,
            zone_length=sudoku_zone_length,
            board=sudoku_initial_board,
        )

        solution_board_fitness = await calculate_board_fitness_single(
            zone_height=sudoku_zone_height,
            zone_length=sudoku_zone_length,
            board=solution_board,
        )

        response_dict = {
            "fitness_score": solution_board_fitness,
            "board_array": solution_board,
        }

        return web.Response(
            body=json.dumps(obj=response_dict, indent=None),
            reason=r"your request was successfully, check the results in the body of this response",
            status=200,
        )

    else:
        print_log(r"the authorization wasn't found or isn't correct", script_firm)
        return web.Response(
            reason=r"you aren't authorized to use this api, check your request Authorization header",
            status=401,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["ACCESS_PORT"]))
