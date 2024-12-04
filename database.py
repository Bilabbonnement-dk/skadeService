import sqlite3

def init_db():
    connection = sqlite3.connect("skadeService.db")
    cursor = connection.cursor()

    # Opret tabel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skadesrapporter (
        rapport_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bil_id INTEGER NOT NULL,
        medarbejder_id INTEGER NOT NULL,
        rapport_dato TEXT NOT NULL,
        skader TEXT,
        omkostninger REAL NOT NULL DEFAULT 0.0
    )
    """)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()

