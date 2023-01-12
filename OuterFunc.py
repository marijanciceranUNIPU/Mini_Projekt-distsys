import aiosqlite
import aiohttp
import numpy as np
import pandas as pd

async def RowFetcher(db):
	cursor = await db.cursor()
	await cursor.execute("SELECT COUNT(*) FROM mini_projekt_db")
	(RowNumber,) = await cursor.fetchone()
	RandomRowIndex = np.random.randint(0, RowNumber, size = 100)
	rows = []
	for rowIndex in RandomRowIndex:
		await cursor.execute("SELECT * FROM mini_projekt_db LIMIT 1 OFFSET %s"%(rowIndex))
		rows.append(await cursor.fetchone())
	return rows

async def WorkerTokenizer(URL, data):
	for index in range(len(data)):
		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			async with session.post(URL, json = data[index]) as response:
				WTResponse = await response.json()
	return WTResponse

async def ForwardToService4(data):
	async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
		async with session.post("http://4.servis:8084/gatherData", json = data) as response:
			Service4Response = await response.json()
	return Service4Response

async def AddToDB():
	try:
		df = pd.read_json('FakeDataset.json', lines = True)
		async with aiosqlite.connect("dbase.db") as db:
			for index, row in df.tail(10000).iterrows():
				await db.execute(
					"INSERT INTO mini_projekt_db (username, ghublink, filename, content) VALUES (?, ?, ?, ?)",
					(
						row.get("repo_name").split("/", 1)[0],
      					"https://github.com/" + row.get("repo_name") + ".com",
                        row.get("path").rsplit("/", 1)[1],
                        row.get("content")
					)
				)
				await db.commit()
		print("Podaci uspješno dodani u bazu.")
	except Exception as e:
		print("Dogodila se greška: ", e)
	pass