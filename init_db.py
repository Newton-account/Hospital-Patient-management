from database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nrc TEXT,
            name TEXT NOT NULL,
            severity INTEGER NOT NULL,
            waiting_time INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    init_db()