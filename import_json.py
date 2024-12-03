import json
import sqlite3

# Connect to SQLite (creates the database file if it doesn't exist)
conn = sqlite3.connect('skader.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Skader')

# Create the Guest table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Skader (
    RapportID INTEGER PRIMARY KEY AUTOINCREMENT,
    BilID INTEGER,
    Beskrivelse TEXT,
    Omkostninger FLOAT,
    Date DATE
)
''')

conn.commit()
# Insert dummy data into the Skader table
cursor.execute('''
INSERT INTO Skader (BilID, Beskrivelse, Omkostninger, Date)
VALUES
(1, 'Scratch on the door', 150.0, '2024-01-01'),
(2, 'Broken headlight', 300.0, '2024-02-15'),
(3, 'Dent on the bumper', 200.0, '2024-03-10')
''')

conn.commit()
conn.close()