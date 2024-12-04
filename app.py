from flask import Flask, request, jsonify
from service.skader import fetch_skade, add_skade, delete_skade

app = Flask(__name__)

########### CRUD method GET ############

# Fetch alle skader
@app.route('/skader', methods=['GET'])
def get_all_skader():
    skader = fetch_skade()
    return jsonify(skader)

# Tilføj en ny skade
@app.route('/skader', methods=['POST'])
def add_new_skade():
    data = request.get_json()
    add_skade(data['bil_id'], data['beskrivelse'], data['pris'], data['dato'])
    return jsonify({"message": "Ny skade tilføjet"}), 201

# Slet en skade
@app.route('/skader/<int:skade_id>', methods=['DELETE'])
def delete_existing_skade(skade_id):
    delete_skade(skade_id)
    return jsonify({"message": "Skade slettet"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)