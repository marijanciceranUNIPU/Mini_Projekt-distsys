import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
    try:
        async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
            task = asyncio.create_task(session.get("http://127.0.0.1:8080/"))
            response = await asyncio.gather(task)
            whole_data = await response[0].json()
            return web.json_response({"name": "service1", "status": "OK", "response": whole_data}, status = 200)
    except Exception as e:
        return web.json_response({"name": "service1", "error" : str(e)}, status = 500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8081)