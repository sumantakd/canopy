import sqlite3, time

def save_snapshot(db_path, root):
    conn = sqlite3.connect(db_path)
    conn.execute("""CREATE TABLE IF NOT EXISTS snapshots
                     (ts INTEGER, path TEXT, size INTEGER)""")
    conn.execute("INSERT INTO snapshots VALUES (?, ?, ?)",
                 (int(time.time()), root.path, root.size))
    conn.commit()
    conn.close()

def last_snapshot(db_path, path):
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT ts, size FROM snapshots WHERE path=? ORDER BY ts DESC LIMIT 1",
        (path,)).fetchone()
    conn.close()
    return row