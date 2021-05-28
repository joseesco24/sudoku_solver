from general_solvers_functions import calculate_board_fitness_report
from general_solvers_functions import calculate_board_fitness_single
from general_solvers_functions import board_random_initialization
from general_solvers_functions import board_random_mutation

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

    print_log(r"starting request headers and body validations", script_firm)

    try:
        await request.json()
        request_header_keys = [key for key in request.headers.keys()]
        api_key = str(os.environ["GENERAL_SOLVER_FUNCTIONS_KEY"])
        request_headers = request.headers
        continue_process = True
        print_log(r"the request headers and body are correct", script_firm)
    except:
        continue_process = False
        print_log(r"the request headers and body are not correct", script_firm)

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

    return continue_process


@api_routes.get(r"/calculate_board_fitness_single")
async def get_board_fitness_single(request: Request):
    continue_process = await check_request_mandatory_requirements(request)
    if continue_process is True:
        request_body = await request.json()
        fitness_score = calculate_board_fitness_single(
            zone_height=request_body["zone_height"],
            zone_length=request_body["zone_length"],
            board=request_body["board"],
        )
        response_dict = {
            "fitness_score": fitness_score,
        }
        headers = {"Content-Type": "application/json"}
        return web.Response(
            body=json.dumps(obj=response_dict, indent=None),
            reason=r"your request was successfully, check the results in the body of this response",
            headers=headers,
            status=200,
        )
    else:
        return web.Response(
            reason=r"your request wasn't successfully, check the container logs for more details",
            status=400,
        )


@api_routes.get(r"/calculate_board_fitness_report")
async def get_board_fitness_report(request: Request):
    continue_process = await check_request_mandatory_requirements(request)
    if continue_process is True:
        request_body = await request.json()
        (
            total_collisions,
            zone_collisions,
            row_collisions,
            column_collisions,
        ) = calculate_board_fitness_report(
            zone_height=request_body["zone_height"],
            zone_length=request_body["zone_length"],
            board=request_body["board"],
        )
        response_dict = {
            "column_collisions": column_collisions,
            "total_collisions": total_collisions,
            "zone_collisions": zone_collisions,
            "row_collisions": row_collisions,
        }
        headers = {"Content-Type": "application/json"}
        return web.Response(
            body=json.dumps(obj=response_dict, indent=None),
            reason=r"your request was successfully, check the results in the body of this response",
            headers=headers,
            status=200,
        )
    else:
        return web.Response(
            reason=r"your request wasn't successfully, check the container logs for more details",
            status=400,
        )


@api_routes.get(r"/board_random_initialization")
async def get_random_initialization(request: Request):
    continue_process = await check_request_mandatory_requirements(request)
    if continue_process is True:
        request_body = await request.json()
        board = board_random_initialization(
            fixed_numbers_board=request_body["fixed_numbers_board"],
            zone_height=request_body["zone_height"],
            zone_length=request_body["zone_length"],
        )
        response_dict = {
            "board": board,
        }
        headers = {"Content-Type": "application/json"}
        return web.Response(
            body=json.dumps(obj=response_dict, indent=None),
            reason=r"your request was successfully, check the results in the body of this response",
            headers=headers,
            status=200,
        )
    else:
        return web.Response(
            reason=r"your request wasn't successfully, check the container logs for more details",
            status=400,
        )


@api_routes.get(r"/board_random_mutation")
async def get_random_mutation(request: Request):
    continue_process = await check_request_mandatory_requirements(request)
    if continue_process is True:
        request_body = await request.json()
        board = board_random_mutation(
            fixed_numbers_board=request_body["fixed_numbers_board"],
            board=request_body["board"],
        )
        response_dict = {
            "board": board,
        }
        headers = {"Content-Type": "application/json"}
        return web.Response(
            body=json.dumps(obj=response_dict, indent=None),
            reason=r"your request was successfully, check the results in the body of this response",
            headers=headers,
            status=200,
        )
    else:
        return web.Response(
            reason=r"your request wasn't successfully, check the container logs for more details",
            status=400,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["ACCESS_PORT"]))
