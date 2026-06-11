import sqlite3

DB_NAME = "database.db"


# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # FINAL APPROVED DATA TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ff_ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        uid TEXT,
        text TEXT
    )
    """)

    # PENDING APPROVAL TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pending (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        uid TEXT,
        text TEXT,
        user_id TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- ADD FINAL DATA ----------------
def add_data(name, uid, text):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ff_ids (name, uid, text)
    VALUES (?, ?, ?)
    """, (name, uid, text))

    conn.commit()
    conn.close()


# ---------------- ADD PENDING DATA ----------------
def add_pending(name, uid, text, user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO pending (name, uid, text, user_id)
    VALUES (?, ?, ?, ?)
    """, (name, uid, text, user_id))

    conn.commit()
    conn.close()


# ---------------- GET ALL APPROVED DATA ----------------
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


# ---------------- DELETE APPROVED DATA ----------------
def delete_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM ff_ids WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()


# ---------------- UPDATE APPROVED DATA ----------------
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


# ---------------- GET PENDING DATA ----------------
def get_pending():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM pending")
    rows = cur.fetchall()
    conn.close()

    return rows


# ---------------- DELETE PENDING DATA ----------------
def delete_pending(pid):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM pending WHERE id = ?", (pid,))

    conn.commit()
    conn.close()


# ---------------- INIT CALL ----------------
init_db()
