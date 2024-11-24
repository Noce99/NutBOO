from flask import Flask, request, jsonify
from flask_cors import CORS
from get_info_gps import GpsLivelox
import json
from pymongo import MongoClient

YEAR = 2024

app = Flask(__name__)
CORS(app)
live_gps = GpsLivelox()
client = MongoClient('mongodb://localhost:27017/')
db = client[f"boo{YEAR}"]
# Collections:
TEAMS = db["teams"]
QUESTIONS = db["questions"]
GPS = db["gps"]

@app.route("/live_gps", methods=["GET"])
def get_live_gps_data():
    gps_id = request.args.get("gps_id", default="", type=str)
    if gps_id == "":
        return "You should specify a gps_id!", 400
    found_gps = list(GPS.find({"gps_id": gps_id}))
    if len(found_gps) == 0:
        return "No GPS whit this gps_id!", 400
    if len(found_gps) > 1:
        return "To many GPS whit this gps_id! WTF?", 400
    my_gps = found_gps[0]
    last_position = my_gps["location"][-1]
    return jsonify(last_position)


@app.route('/login', methods=['POST'])
def post_login():
    content = request.json
    tried_passcode = content["passcode"]
    print(f"LogIn Attempt -> {tried_passcode}")
    found_teams = list(TEAMS.find({"passcode": tried_passcode}))
    if len(found_teams) == 0:
        response = {"team": "Unknown"}
    elif len(found_teams) > 1:
        return "To many TEAMS whit this passcode! WTF?", 400
    else:
        my_team = found_teams[0]
        response = {"team": my_team["name"]}
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
        answer_id = str(content["answer_id"])
        answer = content["answer"]
        with open("answers.json", "r") as answers_file:
            answers = json.load(answers_file)
        print(answers)
        if team_name not in answers.keys():
            answers[team_name] = {}
        print(answers)
        if answer_id not in answers[team_name].keys():
            answers[team_name][answer_id] = []
        print(answers)
        answers[team_name][answer_id].append(answer)
        print(answers)
        with open("answers.json", "w") as answers_file:
            answers_file.write(json.dumps(answers, indent=4))
        response = {"Accepted": answer_id}
    else:
        response = {"team": "Unknown"}
    return jsonify(response)

if __name__ == '__main__':
    live_gps.thread.start()
    app.run(host="0.0.0.0", ssl_context=('cert1.pem', 'privkey1.pem'), port=4989)


