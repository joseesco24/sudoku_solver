from sudoku_hill_climbing import solve_sudoku_using_hill_climbing_algorithm

from sudoku_common_functions import calculate_sudoku_board_fitness_score

from yaml_reader import load_http_response_message
from yaml_reader import load_log_message
from logs_printer import print_log

from aiohttp.web_request import Request
from aiohttp import web
import numpy as np
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()

script_firm = "api"


async def check_request_requirements(request: Request):

    global script_firm

    print_log(load_log_message("lm_009"), script_firm)

    try:
        request_body = await request.json()
        print_log(load_log_message("lm_003"), script_firm)
        continue_process = True
        message_key = "hm_001"
    except:
        print_log(load_log_message("lm_004"), script_firm)
        continue_process = False
        message_key = "hm_002"

    if continue_process is True:
        necessary_fields_in_request = ["board_array", "zone_length", "zone_height"]
        request_header_keys = [key for key in request.headers.keys()]
        request_body_keys = [key for key in request_body.keys()]
        api_key = "7bC47Aa517f3eC4BF7F29ee84dc0D5E3"
        request_headers = request.headers

    if continue_process is True:
        if "Authorization" in request_header_keys:
            print_log(load_log_message("lm_001"), script_firm)
        else:
            print_log(load_log_message("lm_006"), script_firm)
            message_key = "hm_004"
            continue_process = False

    if continue_process is True:
        if api_key == request_headers["Authorization"]:
            print_log(load_log_message("lm_002"), script_firm)
        else:
            print_log(load_log_message("lm_005"), script_firm)
            message_key = "hm_003"
            continue_process = False

    if continue_process is True:
        if type(request_body) is dict:
            print_log(load_log_message("lm_008"), script_firm)
        else:
            print_log(load_log_message("lm_007"), script_firm)
            message_key = "hm_005"
            continue_process = False

    if continue_process is True:
        if all(key in request_body_keys for key in necessary_fields_in_request):
            print_log(load_log_message("lm_012"), script_firm)
        else:
            missing_keys = np.setdiff1d(necessary_fields_in_request, request_body_keys)
            missing_keys_str = ""
            for missing_key in missing_keys:
                missing_keys_str += missing_key + ","
            print_log(load_log_message("lm_013").format(missing_keys_str), script_firm)
            message_key = "hm_006"
            continue_process = False

    if continue_process is True:
        if type(request_body["board_array"]) is list:
            print_log(load_log_message("lm_014").format("board_array"), script_firm)
        else:
            print_log(load_log_message("lm_015").format("board_array"), script_firm)
            message_key = "hm_007"
            continue_process = False

    if continue_process is True:
        if type(request_body["zone_length"]) is int:
            print_log(load_log_message("lm_014").format("zone_length"), script_firm)
        else:
            print_log(load_log_message("lm_015").format("zone_length"), script_firm)
            message_key = "hm_008"
            continue_process = False

    if continue_process is True:
        if type(request_body["zone_height"]) is int:
            print_log(load_log_message("lm_014").format("zone_height"), script_firm)
        else:
            print_log(load_log_message("lm_015").format("zone_height"), script_firm)
            message_key = "hm_009"
            continue_process = False

    if continue_process is True:
        board_dimensions = request_body["zone_height"] * request_body["zone_length"]
        board_height = len(request_body["board_array"])
        if board_dimensions == board_height:
            print_log(load_log_message("lm_016").format("columns"), script_firm)
        else:
            print_log(load_log_message("lm_017").format("columns"), script_firm)
            message_key = "hm_010"
            continue_process = False

    if continue_process is True:
        board_dimensions = request_body["zone_height"] * request_body["zone_length"]
        board_lenght_summation = 0
        for board_row in request_body["board_array"]:
            board_lenght_summation += len(board_row)
        if board_dimensions == board_lenght_summation / board_dimensions:
            print_log(load_log_message("lm_016").format("rows"), script_firm)
        else:
            print_log(load_log_message("lm_017").format("rows"), script_firm)
            message_key = "hm_011"
            continue_process = False

    if continue_process is True:
        print_log(load_log_message("lm_010"), script_firm)
    else:
        print_log(load_log_message("lm_011"), script_firm)

    return continue_process, message_key


@api_routes.get("/solver/hc")
async def solver(request: Request):

    continue_process, message_key = await check_request_requirements(request)
    reason_message = load_http_response_message(message_key)

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


        solution_board = solve_sudoku_using_hill_climbing_algorithm(
            hill_climbing_restarts=restarts,
            hill_climbing_searchs=searchs,
            zone_height=sudoku_zone_height,
            zone_length=sudoku_zone_length,
            board=sudoku_initial_board,
        )

        solution_board_fitness = calculate_sudoku_board_fitness_score(
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
