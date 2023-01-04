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