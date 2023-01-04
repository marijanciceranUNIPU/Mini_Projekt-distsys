import aiohttp
import asyncio
from aiohttp import web
from OuterFunc import WorkerTokenizer

routes = web.RouteTableDef()

@routes.get("/")
async def first_service(request):
    try:
        async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
            task = asyncio.create_task(session.get("http://127.0.0.1:8080/"))
            response = await asyncio.gather(task)
            whole_data = await response[0].json()
            Dictionary = [
                {
                    "id": item[0], 
                    "username": item[1], 
                    "ghublink": item[2], 
                    "filename": item[3]
                } 
                for item in whole_data.get("data")
            ]
            firstWT = await WorkerTokenizer("http://127.0.0.1:8082/", Dictionary)
            secondWT = await WorkerTokenizer("http://127.0.0.1:8083/", Dictionary)
        return web.json_response({"name": "service1", "status": "OK", "response": [whole_data, firstWT, secondWT]}, status = 200)
    except Exception as e:
        return web.json_response({"name": "service1", "error" : str(e)}, status = 500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8081)