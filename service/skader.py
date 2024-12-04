import sqlite3
import os

# Sti til databasen
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'db.sqlite3')

# Forbind til databasen
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returnér rækker som dict-lignende objekter
    return conn

# Hent alle skader
def fetch_skade():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SkadeRapporter")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Tilføj en ny skade
def add_skade(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO SkadeRapporter (bil_id, beskrivelse, pris, dato)
        VALUES (?, ?, ?, ?)
    """, (data['bil_id'], data['beskrivelse'], data['pris'], data['dato']))
    conn.commit()
    conn.close()


# Slet en skade
def delete_skade(skade_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SkadeRapporter WHERE id = ?", (skade_id,))
    conn.commit()
    conn.close()