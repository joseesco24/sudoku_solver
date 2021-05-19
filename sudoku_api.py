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
        print_log(message="The authorization exists", script_firm=script_firm)

        if api_key == str(request_headers["Authorization"]):
            print_log(message="The authorization is valid", script_firm=script_firm)

            if request.body_exists and request.can_read_body:
                print_log(
                    message="The request body is readable", script_firm=script_firm
                )

                request_body = await request.json()
                return web.Response(
                    reason="Your request was successfully, see the results in the body section of this response.",
                    body=json.dumps(obj=request_body, indent=None),
                    status=200,
                )

            else:
                print_log(
                    message="The request body is not readable", script_firm=script_firm
                )
                return web.Response(
                    reason="There was problem reading your request body, please check it before sending again the request.",
                    status=400,
                )


api = web.Application()
api.add_routes(api_routes)
web.run_app(app=api, port=int(os.environ["PORT"]))
