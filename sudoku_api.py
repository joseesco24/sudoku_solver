from aiohttp.web_request import Request
from logs_printer import print_log
from aiohttp import web
import json
import os

script_firm = "API"
api_key = "client_api"

api = web.Application()
api_routes = web.RouteTableDef()


@api_routes.get("/solver")
async def solver(request: Request):

    global api_key, script_firm

    request_headers = request.headers
    request_header_keys = [key for key in request_headers.keys()]

    if "Authorization" in request_header_keys:
        print_log("lm_001", script_firm)

        if api_key == str(request_headers["Authorization"]):
            print_log("lm_002", script_firm)

            if request.body_exists and request.can_read_body:
                print_log("lm_003", script_firm)

                request_body = await request.json()
                return web.Response(
                    reason="hm_001",
                    body=json.dumps(obj=request_body, indent=None),
                    status=200,
                )

            else:
                print_log("lm_004", script_firm)
                return web.Response(
                    reason="hm_002",
                    status=400,
                )


api = web.Application()
api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
