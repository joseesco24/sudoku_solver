from yaml_reader import load_http_response_messages_dict
from yaml_reader import load_log_messages_dict
from aiohttp.web_request import Request
from logs_printer import print_log
from aiohttp import web
import json
import os

api_key = "7bC47Aa517f3eC4BF7F29ee84dc0D5E3"
script_firm = "API"

http_messages = load_http_response_messages_dict()
log_messages = load_log_messages_dict()

api = web.Application()
api_routes = web.RouteTableDef()


@api_routes.get("/solver")
async def solver(request: Request):

    global api_key, script_firm, http_messages, log_messages

    request_headers = request.headers
    request_header_keys = [key for key in request_headers.keys()]

    if "Authorization" in request_header_keys:
        print_log(log_messages["lm_001"], script_firm)

        if api_key == str(request_headers["Authorization"]):
            print_log(log_messages["lm_002"], script_firm)

            if request.body_exists and request.can_read_body:
                print_log(log_messages["lm_003"], script_firm)

                request_body = await request.json()
                return web.Response(
                    reason=http_messages["hm_001"],
                    body=json.dumps(obj=request_body, indent=None),
                    status=200,
                )

            else:
                print_log(log_messages["lm_004"], script_firm)
                return web.Response(
                    reason=http_messages["hm_002"],
                    status=400,
                )

        else:
            print_log(log_messages["lm_005"], script_firm)
            return web.Response(
                reason=http_messages["hm_003"],
                status=401,
            )

    else:
        print_log(log_messages["lm_006"], script_firm)
        return web.Response(
            reason=http_messages["hm_004"],
            status=401,
        )


api = web.Application()
api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
