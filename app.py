from flask import Flask, request, jsonify
from service.skader import fetch_skade

app = Flask(__name__)

########### CRUD method GET ############

@app.route('/skader', methods=['GET'])
def get_all_reviews():
    skader = fetch_skade()
    return jsonify(skader)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)