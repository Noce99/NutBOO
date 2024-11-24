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

@app.route("/live_gps", methods=["POST"])
def get_live_gps_data():
    content = request.json
    print(content)
    if "gps_id" not in content:
        return "You should specify a gps_id!", 400
    gps_id = str(content["gps_id"])
    found_gps = list(GPS.find({"gps_id": gps_id}))
    if len(found_gps) == 0:
        return "No GPS whit this gps_id!", 400
    if len(found_gps) > 1:
        return "To many GPS whit this gps_id! WTF?", 400
    my_gps = found_gps[0]
    last_position = my_gps["location"][-1]
    return jsonify(last_position), 200

@app.route("/login", methods=["POST"])
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
    questions = list(QUESTIONS.find({}, {"_id": 0}))
    return jsonify(questions)

@app.route('/answer', methods=['POST'])
def post_answer():
    content = request.json
    tried_passcode = str(content["passcode"])
    answer_id = str(content["answer_id"])
    answer = str(content["answer"])
    result = TEAMS.update_one(
        {"passcode": tried_passcode, "answers.question_id": answer_id},
        {"$push": {"answers.$.answer": answer}}
    )
    if result.modified_count == 0:
        found_questions = list(QUESTIONS.find(
            {"question_id": answer_id}
        ))
        if len(found_questions) > 1:
            print(f"WTF! More than one question with same id: {answer_id}!")
        elif len(found_questions) == 1:
            TEAMS.update_one(
                {"passcode": tried_passcode},
                {"$push": {"answers": {"question_id": answer_id, "answer": [answer]}}}
            )
    return "OK", 200

if __name__ == '__main__':
    live_gps.thread.start()
    app.run(host="0.0.0.0", ssl_context=('cert1.pem', 'privkey1.pem'), port=4989)


