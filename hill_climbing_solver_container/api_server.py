from general_solver_functions_access import calculate_board_fitness_score
from hill_climbing import solve_using_hill_climbing_algorithm
from general_utilities import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()

script_firm = "api"


async def check_request_mandatory_requirements(request: Request):

    global script_firm

    print_log(r"starting request body validations", script_firm)

    try:
        request_body = await request.json()
        necessary_fields_in_request = ["board_array", "zone_length", "zone_height"]
        request_header_keys = [key for key in request.headers.keys()]
        request_body_keys = [key for key in request_body.keys()]
        api_key = r"7bC47Aa517f3eC4BF7F29ee84dc0D5E3"
        request_headers = request.headers
        continue_process = True
        print_log(r"the request body is correct", script_firm)
    except:
        continue_process = False
        print_log(r"the request body is not correct", script_firm)

    # Authorization header validations.

    if continue_process is True:
        if "Authorization" in request_header_keys:
            print_log(r"the authorization header exists", script_firm)
        else:
            print_log(r"the authorization header dosn't exists", script_firm)
            continue_process = False
    if continue_process is True:
        if api_key == request_headers["Authorization"]:
            print_log(r"the authorization header is valid", script_firm)
        else:
            print_log(r"the authorization header isn't valid", script_firm)
            continue_process = False

    # Mandatory parameters existanse validations.

    if continue_process is True:
        if all(key in request_body_keys for key in necessary_fields_in_request):
            print_log(r"the request body have all necesary labels", script_firm)
        else:
            print_log(r"the request body dosn't have all necessary labels", script_firm)
            continue_process = False

    # Mandatory parameters type validations.

    if continue_process is True:
        if type(request_body["board_array"]) is list:
            print_log(
                r"the variable board_array has the correct data type", script_firm
            )
        else:
            print_log(
                r"the variable board_array hasn't the correct data type", script_firm
            )
            continue_process = False
    if continue_process is True:
        if type(request_body["zone_length"]) is int:
            print_log(
                r"the variable zone_length has the correct data type", script_firm
            )
        else:
            print_log(
                r"the variable zone_length hasn't the correct data type", script_firm
            )
            continue_process = False
    if continue_process is True:
        if type(request_body["zone_height"]) is int:
            print_log(
                r"the variable zone_height has the correct data type", script_firm
            )
        else:
            print_log(
                r"the variable zone_height hasn't the correct data type", script_firm
            )
            continue_process = False

    # Board dimensions validations.

    if continue_process is True:
        board_dimensions = request_body["zone_height"] * request_body["zone_length"]
        board_height = len(request_body["board_array"])
        if board_dimensions == board_height:
            print_log(r"the board columns dimensions are correct", script_firm)
        else:
            print_log(r"the board columns dimensions aren't correct", script_firm)
            continue_process = False
    if continue_process is True:
        board_dimensions = request_body["zone_height"] * request_body["zone_length"]
        board_lenght_summation = 0
        for board_row in request_body["board_array"]:
            board_lenght_summation += len(board_row)
        if board_dimensions == board_lenght_summation / board_dimensions:
            print_log(r"the board rows dimensions are correct", script_firm)
        else:
            print_log(r"the board rows dimensions aren't correct", script_firm)
            continue_process = False

    if continue_process is True:
        print_log(r"request body validation end successfully", script_firm)
    else:
        print_log(r"request body validation dosn't end successfully", script_firm)

    return continue_process


@api_routes.get(r"/solver/hc")
async def solver(request: Request):

    continue_process = await check_request_mandatory_requirements(request)

    if continue_process is True:

        restarts, searchs = 10, 10

        request_body = await request.json()
        request_body_keys = [key for key in request_body.keys()]

        sudoku_initial_board = request_body["board_array"]
        sudoku_zone_height = request_body["zone_height"]
        sudoku_zone_length = request_body["zone_length"]

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

        solution_board = solve_using_hill_climbing_algorithm(
            hill_climbing_restarts=restarts,
            hill_climbing_searchs=searchs,
            zone_height=sudoku_zone_height,
            zone_length=sudoku_zone_length,
            board=sudoku_initial_board,
        )

        solution_board_fitness = calculate_board_fitness_score(
            zone_height=sudoku_zone_height,
            zone_length=sudoku_zone_length,
            board=solution_board,
        )

        response_dict = {
            "board_array": solution_board,
            "fitness_score": solution_board_fitness,
        }

        return web.Response(
            body=json.dumps(obj=response_dict, indent=None),
            reason=r"your request was successfully, check the results in the body of this response",
            status=200,
        )

    else:
        return web.Response(
            reason=r"your request wasn't successfully, check the container logs for more details",
            status=400,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
