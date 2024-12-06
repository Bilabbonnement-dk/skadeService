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

######### url for Lejeaftale Service #########
LEJEAFTALE_SERVICE_URL = "http://localhost:5002"



############   Functionallity behind the Calculation of damages related to LajeaftaleID and KundeID   ##########

##  Get customer id from lejeaftale service  ##

#Send a POST request to LejeaftaleService to fetch KundeID and BilID for a given LejeaftaleID.
def get_data_from_agreement_service(lejeaftaleID):
    
    # Validate input
    if not lejeaftaleID or not isinstance(lejeaftaleID, int):
        return {"error": "Invalid or missing field: 'lejeaftaleID'"}, 400

    try:
        # Construct the payload
        payload = {"lejeaftale_id": lejeaftaleID}

        # Send the POST request to Lejeaftale Service
        response = requests.post(f"{LEJEAFTALE_SERVICE_URL}/process-kunde-data", json=payload)

        # Handle response from Lejeaftale Service
        if response.status_code == 200:
            return response.json(), 200
        elif response.status_code == 404:
            return {"error": f"No data found for LejeaftaleID {lejeaftaleID}"}, 404
        else:
            return {"error": f"Unexpected response: {response.text}"}, response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to lejeaftale service: {str(e)}"}, 500

##  Calculate full price of damages related to a single lejeaftaleID  ##

def calculate_pris(lejeaftale_id):

    try:
    # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch data for the provided LejeaftaleID
        query = "SELECT LejeaftaleID, Omkostninger, Beskrivelse FROM Skader WHERE LejeaftaleID = ?"

        cursor.execute(query, (lejeaftale_id,))
        results = cursor.fetchall()
        conn.close()

        # Handle no data found
        if not results:
            return {"error": f"No damages found for LejeaftaleID {lejeaftale_id}"}, 404 
        
        # List of damages for the same lejeaftale id
        damages_list = [ {"Beskrivelse": row["Beskrivelse"], "Omkostninger": row["Omkostninger"]} for row in results ]

        # calculate sum of all damages found 
        total_cost = sum(row["Omkostninger"] for row in results)

        return {
            "lejeaftale_id": lejeaftale_id,
            "damages": damages_list,
            "total_cost": total_cost
        }, 200

    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500
    

print(calculate_pris(4))



############   Functionallity behind    ##########

def add_damage_report_send_from_lejeaftaleService(data):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert damage report into the database
        query = """
            INSERT INTO Skader (BilID, LejeAftaleID, Beskrivelse, Omkostninger)
            VALUES (?, ?, ?, ?)
        """

        # Execute the query
        cursor.execute(query, (data['BilID'], data['LejeAftaleID'], data['Beskrivelse'], data['Omkostninger']))

        conn.commit()

        # Fetch the last inserted ID
        damage_id = cursor.lastrowid
        conn.close()


        # Returning success message
        return {
            "message": "Damage report added successfully",
            "damage_id": damage_id
        }, 201
    
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}, 500


