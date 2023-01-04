import aiohttp
from aiohttp import web

Code = []

routes = web.RouteTableDef()

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8084)