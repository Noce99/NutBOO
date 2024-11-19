from flask import Flask, request, jsonify
from flask_cors import CORS
from get_info_gps import GpsLivelox
import json
app = Flask(__name__)
CORS(app)
live_gps = GpsLivelox()


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
    with open("questions_and_answers.json", "r") as qa_file:
        qa = json.load(qa_file)
    return jsonify(qa)

@app.route('/answer', methods=['POST'])
def post_answer():
    content = request.json
    tried_passcode = content["passcode"]
    with open("teams.json", "r") as teams_file:
        users = json.load(teams_file)
    if tried_passcode in users.keys():
        team_name =  users[tried_passcode]
        answer_id = content["answer_id"]
        answer = content["answer"]
        with open("answers.json", "r") as answers_file:
            answers = json.load(answers_file)
        if team_name not in answers.keys():
            answers[team_name] = {}
        if answer_id not in answers[team_name].keys():
            answers[team_name][answer_id] = []
        else:
            print(answers[team_name][answer_id])
        print(answers[team_name][answer_id])
        answers[team_name][answer_id].append(answer)
        print(answers[team_name][answer_id])
        with open("answers.json", "w") as answers_file:
            answers_file.write(json.dumps(answers, indent=4))
        response = {"Accepted": answer_id}
    else:
        response = {"team": "Unknown"}
    return jsonify(response)

if __name__ == '__main__':
    live_gps.thread.start()
    app.run(host="0.0.0.0", ssl_context=('cert1.pem', 'privkey1.pem'), port=4989)


