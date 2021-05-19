from yaml_reader import load_http_response_message
from yaml_reader import load_log_message
from logs_printer import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_routes = web.RouteTableDef()
api = web.Application()

script_firm = "api"


async def check_request_requirements(request: Request):

    global script_firm

    necessary_fields_in_request = ["board_array", "zone_length", "zone_height"]
    api_key = "7bC47Aa517f3eC4BF7F29ee84dc0D5E3"

    request_body = await request.json()
    request_body_keys = [key for key in request_body.keys()]

    request_headers = request.headers
    request_header_keys = [key for key in request_headers.keys()]

    continue_process = True
    message_key = "hm_001"

    if continue_process is True:
        if request.body_exists:
            print_log(load_log_message("lm_003"), script_firm)
        else:
            print_log(load_log_message("lm_004"), script_firm)
            message_key = "hm_002"
            continue_process = False

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
            print_log(load_log_message("lm_008"), script_firm)
            message_key = "hm_005"
            continue_process = False

    if continue_process is True:
        if all(key in request_body_keys for key in necessary_fields_in_request):
            pass
        else:
            continue_process = False

    if continue_process is True:
        if type(request_body["board_array"]) is list:
            pass
        else:
            continue_process = False

    if continue_process is True:
        if type(request_body["zone_length"]) is int:
            pass
        else:
            continue_process = False

    if continue_process is True:
        if type(request_body["zone_height"]) is int:
            pass
        else:
            continue_process = False

    return continue_process, message_key


@api_routes.get("/solver/ga")
async def solver(request: Request):

    continue_process, message_key = await check_request_requirements(request)
    reason_message = load_http_response_message(message_key)

    if continue_process is True:
        request_body = await request.json()
        return web.Response(
            body=json.dumps(obj=request_body, indent=None),
            reason=reason_message,
            status=200,
        )

    else:
        return web.Response(
            reason=reason_message,
            status=400,
        )


@api_routes.get("/solver/hc")
async def solver(request: Request):

    continue_process, message_key = await check_request_requirements(request)
    reason_message = load_http_response_message(message_key)

    if continue_process is True:
        request_body = await request.json()
        return web.Response(
            body=json.dumps(obj=request_body, indent=None),
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
