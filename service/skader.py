import json
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('skader.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_skade():
    conn = get_db_connection()
    skader = conn.execute('SELECT * FROM Skader').fetchall()
    conn.close()
    return skader