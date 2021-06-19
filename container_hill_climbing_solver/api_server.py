from general_solver_functions_access import calculate_board_fitness_report

from hill_climbing import solve_using_hill_climbing_algorithm

from general_utilities import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()

script_firm = "api"


@api_routes.get(r"/health_test")
async def health_test(request: Request):

    origin_url = f"{request.scheme}://{request.remote}{request.rel_url}"

    print_log(f"incoming health test request form {origin_url}", script_firm)
    print_log(
        f"responding health test request from {origin_url} with status code 200",
        script_firm,
    )

    return web.Response(
        status=200,
    )


@api_routes.get(r"/solver")
async def solver(request: Request):

    request_header_keys = [key for key in request.headers.keys()]

    if (
        "Authorization" in request_header_keys
        and request.headers["Authorization"] == os.environ["ACCESS_KEY"]
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

        solution_board = await solve_using_hill_climbing_algorithm(
            hill_climbing_restarts=restarts,
            hill_climbing_searchs=searchs,
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
            status=200,
        )

    else:
        print_log(r"the authorization wasn't found or isn't correct", script_firm)
        return web.Response(
            reason=r"you aren't authorized to use this api",
            status=401,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["ACCESS_PORT"]))