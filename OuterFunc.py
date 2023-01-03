import aiosqlite
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