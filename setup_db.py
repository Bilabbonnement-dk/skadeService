import sqlite3
import os

# Sti til databasen
DB_PATH = 'database/db.sqlite3'

def create_database():
    # Tjek, om mappen "database" findes
    if not os.path.exists('database'):
        os.makedirs('database')

    # Forbind til databasen
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Opret tabellen SkadeRapporter
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SkadeRapporter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bil_id INTEGER NOT NULL,
            beskrivelse TEXT NOT NULL,
            pris REAL NOT NULL,
            dato TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"Databasen er opsat og findes på: {DB_PATH}")

# Kør denne funktion for at opsætte databasen
if __name__ == "__main__":
    create_database()
