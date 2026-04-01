import sqlite3

DB_NAME = "hospital.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nrc TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            severity TEXT,
            waiting_time INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    conn.commit()
    conn.close()