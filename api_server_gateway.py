from general_solvers_functions import calculate_board_fitness_score
from greedy_solver import solve_using_hill_climbing_algorithm
from general_utility_functions import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()

script_firm = "api"


async def check_request_mandatory_requirements(request: Request):

    global script_firm

    print_log("starting request body validations", script_firm)

    try:
        request_body = await request.json()
        print_log("the request body is readable", script_firm)
        continue_process = True
        reason_message = "your request was successfully"
    except:
        print_log("the request body isn't readable", script_firm)
        continue_process = False
        reason_message = "there was problem reading your request body"

    if continue_process is True:
        necessary_fields_in_request = ["board_array", "zone_length", "zone_height"]
        request_header_keys = [key for key in request.headers.keys()]
        request_body_keys = [key for key in request_body.keys()]
        api_key = "7bC47Aa517f3eC4BF7F29ee84dc0D5E3"
        request_headers = request.headers

    # Authorization header validations.

    if continue_process is True:
        if "Authorization" in request_header_keys:
            print_log("the authorization header exists", script_firm)
        else:
            print_log("the authorization header dosn't exists", script_firm)
            reason_message = "the authorization header could not be found, please check it and include the authorization header before sending again the request"
            continue_process = False

    if continue_process is True:
        if api_key == request_headers["Authorization"]:
            print_log("the authorization header is valid", script_firm)
        else:
            print_log("the authorization header isn't valid", script_firm)
            reason_message = "the authorization header is not valid"
            continue_process = False

    # Body general validations.

    if continue_process is True:
        if type(request_body) is dict:
            print_log("the request body is correct", script_firm)
        else:
            print_log("the request body is not correct", script_firm)
            reason_message = "the request body is not correct"
            continue_process = False

    # Mandatory parameters existanse validations.

    if continue_process is True:
        if all(key in request_body_keys for key in necessary_fields_in_request):
            print_log("the request body have all necesary labels", script_firm)
        else:
            print_log("the request body dosn't have all necessary labels", script_firm)
            reason_message = "the request body does not have all necesary labels"
            continue_process = False

    # Mandatory parameters type validations.

    if continue_process is True:
        if type(request_body["board_array"]) is list:
            print_log("the variable board_array has the correct data type", script_firm)
        else:
            print_log(
                "the variable board_array hasn't the correct data type", script_firm
            )
            reason_message = "the board in your request body is not a list, check it before send it again"
            continue_process = False

    if continue_process is True:
        if type(request_body["zone_length"]) is int:
            print_log("the variable zone_length has the correct data type", script_firm)
        else:
            print_log(
                "the variable zone_length hasn't the correct data type", script_firm
            )
            reason_message = "the zone length in your request body is not a int, check it before send it again"
            continue_process = False

    if continue_process is True:
        if type(request_body["zone_height"]) is int:
            print_log("the variable zone_height has the correct data type", script_firm)
        else:
            print_log(
                "the variable zone_height hasn't the correct data type", script_firm
            )
            reason_message = "the zone height in your request body is not a int, check it before send it again"
            continue_process = False

    # Board dimensions validations.

    if continue_process is True:

        board_dimensions = request_body["zone_height"] * request_body["zone_length"]
        board_height = len(request_body["board_array"])

        if board_dimensions == board_height:
            print_log("the board columns dimensions are correct", script_firm)
        else:
            print_log("the board columns dimensions aren't correct", script_firm)
            reason_message = "the board columns dimensions of your request are not correct, please check it before send your request again"
            continue_process = False

    if continue_process is True:

        board_dimensions = request_body["zone_height"] * request_body["zone_length"]
        board_lenght_summation = 0
        for board_row in request_body["board_array"]:
            board_lenght_summation += len(board_row)

        if board_dimensions == board_lenght_summation / board_dimensions:
            print_log("the board rows dimensions are correct", script_firm)
        else:
            print_log("the board rows dimensions aren't correct", script_firm)
            reason_message = "the board rows dimensions of your request are not correct, please check it before send your request again"
            continue_process = False

    if continue_process is True:
        print_log("request body validation end successfully", script_firm)
    else:
        print_log("request body validation dosn't end successfully", script_firm)

    return continue_process, reason_message


@api_routes.get("/solver/hc")
async def solver(request: Request):

    continue_process, reason_message = await check_request_mandatory_requirements(
        request
    )

    if continue_process is True:

        restarts, searchs = 10, 10

        request_body = await request.json()
        request_body_keys = [key for key in request_body.keys()]

        sudoku_initial_board = request_body["board_array"]
        sudoku_zone_height = request_body["zone_height"]
        sudoku_zone_length = request_body["zone_length"]

        if "restarts" in request_body_keys:
            restarts = request_body["restarts"]
        if "searchs" in request_body_keys:
            searchs = request_body["searchs"]

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
            reason=reason_message,
            status=200,
        )

    else:
        return web.Response(
            reason=reason_message,
            status=400,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
