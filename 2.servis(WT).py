import aiohttp
from aiohttp import web
from OuterFunc import ForwardToService4

responses = []

routes = web.RouteTableDef()

@routes.post("/")
async def second_service(request):
	global responses
	try:
		ResData = await request.json()
		if ResData.get("username").lower().startswith("w"):
			response = await ForwardToService4(ResData)
			print(response)
			responses.append(response)
		return web.json_response({"name": "Service 2", "status": "OK", "Service 4 response": responses}, status = 200)
	except Exception as e:
		return web.json_response({"name": "Service 2", "error": str(e)}, status = 500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8082)