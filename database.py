
import aiosqlite

async def init_db():
    async with aiosqlite.connect("ff.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS ff_ids(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            uid TEXT,
            note TEXT
        )
        """)
        await db.commit()

async def add_ff(name, uid, note):
    async with aiosqlite.connect("ff.db") as db:
        await db.execute(
            "INSERT INTO ff_ids(name,uid,note) VALUES(?,?,?)",
            (name,uid,note)
        )
        await db.commit()
