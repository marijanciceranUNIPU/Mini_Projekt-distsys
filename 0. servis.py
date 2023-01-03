import aiohttp
import aiosqlite
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
async def json_data(request):
    try:
        async with aiosqlite.connect("dbase.db") as db:
            async with db.execute("SELECT COUNT(*) FROM mini_projekt_db") as cursor:
                async for row in cursor:
                    if row[0] == 0:
                        data = print("Baza je prazna.")
                    else:
                        data = print("Baza nije prazna.")
        return web.json_response({"name": "service0", "status": "OK", "data": data}, status = 200)
    except Exception as e:
        return web.json_response({"name": "service0", "error": str(e)}, status = 500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8080)
