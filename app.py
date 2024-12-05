from flask import Flask, request, jsonify
import requests

from Service.skader import fetch_damage_reports 
from Service.skader import add_damage_report
from Service.skader import delete_damage_report

app = Flask(__name__)

########### CRUD method GET ############

# Fetch alle skader
@app.route('/skadeRapporter', methods=['GET'])
def get_all_reports():
    reports = fetch_damage_reports()
    return jsonify(reports)

# Tilføj en ny skade
@app.route('/skadeRapporter', methods=['POST'])
def add_new_damages_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid json data"}), 400
    
    result, status_code = add_damage_report(data)
    return jsonify(result), status_code


# Slet en skade
@app.route('/skadeRapporter/<int:reportID>', methods=['DELETE'])
def delete_damages_reports(reportID):
    # Parse JSON body
    data = request.get_data

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # Call the update function with required data
    result, status_code = delete_damage_report({"report_id": reportID})
    return jsonify(result), status_code


# recieve data from Lejeaftale Service
@app.route('/send-data', methods=['GET'])
def send_data():
    # Data to be sent to Service B
    payload = {"data": "Hello from Skades service!"}

    # Send POST request to Service B
    try:
        response = requests.post('http://localhost:5002/process-data', json=payload)
        response_data = response.json()
        return jsonify({"status": "success", "response": response_data}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)