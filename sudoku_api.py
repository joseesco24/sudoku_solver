from logging import error
from yaml_reader import load_http_response_messages_dict
from yaml_reader import load_log_messages_dict
from logs_printer import print_log

from aiohttp.web_request import Request
from aiohttp import web
import json
import os

api_key = "7bC47Aa517f3eC4BF7F29ee84dc0D5E3"
script_firm = "api"

http_messages = load_http_response_messages_dict()
log_messages = load_log_messages_dict()

api_routes = web.RouteTableDef()
api = web.Application()


def check_if_request_body_is_correct(request_body: dict) -> bool:
    request_body_keys = [key for key in request_body.keys()]
    return True


@api_routes.get("/solver")
async def solver(request: Request):

    request_body = await request.json()

    request_headers = request.headers
    request_header_keys = [key for key in request_headers.keys()]

    error_message_key = None
    continue_process = True

    if continue_process is True:
        if "Authorization" in request_header_keys:
            print_log(log_messages["lm_001"], script_firm)
        else:
            print_log(log_messages["lm_006"], script_firm)
            error_message_key = "hm_004"
            continue_process = False

    if continue_process is True:
        if api_key == request_headers["Authorization"]:
            print_log(log_messages["lm_002"], script_firm)
        else:
            print_log(log_messages["lm_005"], script_firm)
            error_message_key = "hm_003"
            continue_process = False

    if continue_process is True:
        if request.body_exists:
            print_log(log_messages["lm_003"], script_firm)
        else:
            print_log(log_messages["lm_004"], script_firm)
            error_message_key = "hm_002"
            continue_process = False

    if continue_process is True:
        if check_if_request_body_is_correct(request_body):
            print_log(log_messages["lm_008"], script_firm)
        else:
            print_log(log_messages["lm_007"], script_firm)
            error_message_key = "hm_005"
            continue_process = False

    if continue_process is True and error_message_key is None:
        return web.Response(
            reason=http_messages["hm_001"],
            body=json.dumps(obj=request_body, indent=None),
            status=200,
        )

    elif continue_process is False and error_message_key is not None:
        return web.Response(
            reason=http_messages[error_message_key],
            status=400,
        )


api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
