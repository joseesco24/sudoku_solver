from aiohttp import web

script_firm = "API"

api = web.Application()
api_routes = web.RouteTableDef()


@api_routes.get("/")
async def hello(request):
    return web.Response(text="Hello, world")


api = web.Application()
api.add_api_routes(api_routes)
web.run_app(app=api, port=3000)
