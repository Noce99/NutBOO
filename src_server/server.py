from flask import Flask, request, jsonify
from flask_cors import CORS
from get_info_gps import GpsLivelox
import json
app = Flask(__name__)
CORS(app)
live_gps = GpsLivelox()

QA = None


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Ciao dal server Python!'}
    return jsonify(data)


@app.route("/live_gps", methods=["GET"])
def live_gps_aa():
    data = {"lat": live_gps.lat, "lon": live_gps.lon}
    return jsonify(data)


@app.route('/api/data', methods=['POST'])
def post_data():
    content = request.json
    response = {'received': content}
    return jsonify(response)


@app.route('/login', methods=['POST'])
def post_login():
    content = request.json
    tried_passcode = content["passcode"]
    print(f"LogIn Attempt -> {tried_passcode}")
    with open("teams.json", "r") as teams_file:
        users = json.load(teams_file)
    if tried_passcode in users.keys():
        response = {"team": users[tried_passcode]}
    else:
        response = {"team": "Unknown"}
    return jsonify(response)

@app.route("/qa", methods=["GET"])
def get_qa():
    return jsonify(QA)

if __name__ == '__main__':
    with open("questions_and_answers.json", "r") as qa_file:
        QA = json.load(qa_file)
    live_gps.thread.start()
    app.run(host="0.0.0.0", ssl_context=('cert1.pem', 'privkey1.pem'), port=4989)


