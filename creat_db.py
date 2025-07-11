import sqlite3

conn = sqlite3.connect("database.db")
db = conn.cursor()

db.execute("""
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    event_name TEXT NOT NULL,
    event_url TEXT,
    user_id INTEGER
);
""")

conn.commit()
conn.close()

