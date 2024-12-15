from flask import Flask, request, jsonify
import requests

from Service.skader import fetch_damage_reports 
from Service.skader import add_damage_report
from Service.skader import delete_damage_report
from Service.connections import get_data_from_agreement_service
from Service.connections import calculate_pris
from Service.connections import add_damage_report_send_from_lejeaftaleService
from Service.connections import send_damage_niveau

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
    


# recieve data from Lejeaftale Service
@app.route('/send-kunde-data/<int:lejeaftaleID>', methods=['GET'])
def send_request(lejeaftaleID):

    agreement_data, agreement_status_code = get_data_from_agreement_service(lejeaftaleID)
    if agreement_status_code != 200:
        return jsonify(agreement_data), agreement_status_code

    cal_data, cal_status_code = calculate_pris(lejeaftaleID)
    if cal_status_code != 200:
        return jsonify(cal_data), agreement_status_code
    
    # format the results
    response = {
        "Agreement_data": agreement_data,
        "Sum_of_damages": cal_data
    }

    return jsonify(response), 200

# Preocess data to Skades Service
@app.route('/process-damage-data', methods=['POST'])
def process_kunde_data():

    # Retrieve json payload
    data = request.json

    # Validate input
    required_fields = {'BilID', 'LejeAftaleID', 'Beskrivelse', 'Omkostninger'}
    if not data or not required_fields:
        return jsonify({"error": "Invalid json data or missing required field"}), 400

    # Call the service function to get data
    result, status_code = add_damage_report_send_from_lejeaftaleService(data)
    
    return jsonify(result), status_code

# Send data to Rapport Service
@app.route('/send-skade-data', defaults={'damage_niveau': None}, methods=['GET'])
@app.route('/send-skade-data/<int:damage_niveau>', methods=['GET'])
def send_skade_data(damage_niveau):
    # Call send_damage_niveau with or without damage_niveau
    report_data, report_status_code = send_damage_niveau(damage_niveau)
    
    # If any error, return it immediately
    if report_status_code != 200:
        return jsonify(report_data), report_status_code

    # Return the response data formatted
    response = { "Damage_data": report_data }
    return jsonify(response), 200





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)