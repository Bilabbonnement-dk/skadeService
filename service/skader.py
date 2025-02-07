import sqlite3
import os
import requests

# Path to the database file
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../database/skader.db')

############   Database connection function   ##########

def get_db_connection():
    #Establish and return a database connection.
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn



############   Fetch all damages   ##########

def fetch_damage_reports():
    # Connect to the database and fetch damage data
    conn = get_db_connection()
    cursor = conn.cursor()

     # Execute a query to fetch all records from the agreement table
    cursor.execute("SELECT * FROM Skader")
    rows = cursor.fetchall()
    conn.close()

    # Convert data to a list of dictionaries with required fields
    filtered_reports = [
        {
        "skade_id": row["RapportID"],
        "bil_id": row["BilID"],
        "lejeaftale_id": row["LejeAftaleID"],
        "beskrivelse": row["Beskrivelse"],
        "omkostninger": row["Omkostninger"],
        "skade_niveau": row["SkadeNiveau"],
        "date": row["Date"]
    } 
    for row in rows
    ]
    
    return filtered_reports

# Fetch and print the filtered damage report data
damage_report_data = fetch_damage_reports()

#print(guests_data)


# Add a new Skade
def add_damage_report(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Skader (BilID, LejeaftaleID, Beskrivelse, Omkostninger, SkadeNiveau)
        VALUES (?, ?, ?, ?, ?)
    """, (data['BilID'], data['LejeaftaleID'], data['Beskrivelse'], data['Omkostninger'], data['SkadeNiveau']))
    conn.commit()
    conn.close()


############   Create new report data   ##########

def add_damage_report(data):
    # Validate input
    required_fields = ['BilID', 'LejeAftaleID', 'Beskrivelse', 'Omkostninger', 'SkadeNiveau']
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields"}, 400


    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Insert new agreement
        cursor.execute(
            "INSERT INTO Skader (BilID, LejeAftaleID, Beskrivelse, Omkostninger, SkadeNiveau)"
            "VALUES (?, ?, ?, ?, ?)", 
            (data['BilID'], data['LejeAftaleID'], data['Beskrivelse'], data['Omkostninger'], data['SkadeNiveau'])
        )
        
        report_id = cursor.lastrowid

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return {"error": f"Database error: {e}"}, 500
    finally:
        conn.close()

    return {
        "message": "Damage report created successfully",
        "report_id": report_id
    }, 201




############   Delete report data   ##########

# Delete Skade
def delete_damage_report(data):

    reportID = data.get('report_id')

    if not reportID:
        return {"error": "Missing required fields: 'report_id'"}, 400
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Skader WHERE RapportID = ?", (reportID,)
            )
        conn.commit()

         # Check if any row was updated
        if cursor.rowcount == 0:
            return {"error": "No report found with the given ID"}, 404

    return {"message": "Report succesfully deleted"}, 200

