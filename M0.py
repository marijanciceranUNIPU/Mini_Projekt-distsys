import aiosqlite
import pandas as pd
from aiohttp import web
from OuterFunc import RowFetcher

routes = web.RouteTableDef()

@routes.get("/")
async def json_data(request):
    try:
        async with aiosqlite.connect("dbase.db") as db:
            async with db.execute("SELECT COUNT(*) FROM mini_projekt_db") as cursor:
                async for row in cursor:
                    if row[0] == 0:
                        print("Baza je prazna.")
                        try:
                            dataframe = pd.read_json("file-000000000040.json", lines = True)
                            async with aiosqlite.connect("dbase.db") as db:
                                for row in dataframe.tail(10000).iterrows():
                                    await db.execute(
                                        "INSERT INTO mini_projekt_db (username, ghublink, filename) VALUES (?, ?, ?)",
                                        (
                                            row.get["repo_name"].rsplit("/", 1)[0],
                                            "https://github.com/" + row.get("repo_name") + ".com",
                                            row.get("path").rsplit("/", 1)[1],
                                            row.get("content")
                                        )
                                    )
                                    await db.commit()
                            data = await RowFetcher(db)
                            print("Podaci uspješno dodani u bazu.", "data: ", data)
                        except Exception as e:
                            print("Dogodila se greška: ", e)
                        pass
                    else:
                        print("Baza nije prazna.")
        return web.json_response({"name": "service0", "status": "OK"}, status = 200)
    except Exception as e:
        return web.json_response({"name": "service0", "error": str(e)}, status = 500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8080)
