import sqlite3

DB_NAME = "database.db"


# ---------------- CREATE TABLE ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ff_ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        uid TEXT,
        text TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- ADD DATA ----------------
def add_data(name, uid, text):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ff_ids (name, uid, text)
    VALUES (?, ?, ?)
    """, (name, uid, text))

    conn.commit()
    conn.close()


# ---------------- GET ALL DATA ----------------
def get_all():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM ff_ids")
    rows = cur.fetchall()
    conn.close()

    data = {}
    for row in rows:
        data[row[0]] = {
            "name": row[1],
            "uid": row[2],
            "text": row[3]
        }

    return data


# ---------------- DELETE DATA ----------------
def delete_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM ff_ids WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()


# ---------------- GET SINGLE DATA ----------------
def get_one(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM ff_ids WHERE id = ?", (user_id,))
    row = cur.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "uid": row[2],
            "text": row[3]
        }
    return None


# ---------------- UPDATE DATA ----------------
def update_data(user_id, name=None, uid=None, text=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if name:
        cur.execute("UPDATE ff_ids SET name = ? WHERE id = ?", (name, user_id))

    if uid:
        cur.execute("UPDATE ff_ids SET uid = ? WHERE id = ?", (uid, user_id))

    if text:
        cur.execute("UPDATE ff_ids SET text = ? WHERE id = ?", (text, user_id))

    conn.commit()
    conn.close()


# ---------------- INIT CALL ----------------
init_db()
