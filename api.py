from yaml_reader import load_http_response_message
from yaml_reader import load_log_message
from logs_printer import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_key = "7bC47Aa517f3eC4BF7F29ee84dc0D5E3"
script_firm = "api"

api_routes = web.RouteTableDef()
api = web.Application()


def check_request_body(request_body: dict) -> bool:

    requiered_keys = ["board", "area"]
    the_request_body_is_correct = True

    if the_request_body_is_correct is True:
        if not type(request_body) is dict:
            the_request_body_is_correct = False

    if the_request_body_is_correct is True:
        request_body_keys = [key for key in request_body.keys()]
        if not all(key in request_body_keys for key in requiered_keys):
            the_request_body_is_correct = False

    if the_request_body_is_correct is True:
        if not type(request_body["board"]) is list:
            the_request_body_is_correct = False

    if the_request_body_is_correct is True:
        if not type(request_body["area"]) is list:
            the_request_body_is_correct = False

    if the_request_body_is_correct is True:
        if not len(request_body["area"]) == 2:
            the_request_body_is_correct = False

    return the_request_body_is_correct


@api_routes.get("/solver")
async def solver(request: Request):

    request_body = await request.json()

    request_headers = request.headers
    request_header_keys = [key for key in request_headers.keys()]

    error_message_key = None
    continue_process = True

    if continue_process is True:
        if "Authorization" in request_header_keys:
            print_log(load_log_message("lm_001"), script_firm)
        else:
            print_log(load_log_message("lm_006"), script_firm)
            error_message_key = "hm_004"
            continue_process = False

    if continue_process is True:
        if api_key == request_headers["Authorization"]:
            print_log(load_log_message("lm_002"), script_firm)
        else:
            print_log(load_log_message("lm_005"), script_firm)
            error_message_key = "hm_003"
            continue_process = False

    if continue_process is True:
        if request.body_exists:
            print_log(load_log_message("lm_003"), script_firm)
        else:
            print_log(load_log_message("lm_004"), script_firm)
            error_message_key = "hm_002"
            continue_process = False

    if continue_process is True:
        if check_request_body(request_body):
            print_log(load_log_message("lm_008"), script_firm)
        else:
            print_log(load_log_message("lm_007"), script_firm)
            error_message_key = "hm_005"
            continue_process = False

    if continue_process is True and error_message_key is None:
        return web.Response(
            reason=load_http_response_message("hm_001"),
            body=json.dumps(obj=request_body, indent=None),
            status=200,
        )

    elif continue_process is False and error_message_key is not None:
        return web.Response(
            reason=load_http_response_message(error_message_key),
            status=400,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
