import shutil
from datetime import datetime

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from get_info_gps import GpsLivelox
import json
from pymongo import MongoClient
import os
import pathlib
import cv2

YEAR = 2024

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 16 MB
CORS(app)
live_gps = GpsLivelox()
client = MongoClient('mongodb://localhost:27017/')
db = client[f"boo{YEAR}"]
# Collections:
TEAMS = db["teams"]
QUESTIONS = db["questions"]
GPS = db["gps"]
NUTBUS_FOLDER = pathlib.Path(__file__).parent.resolve().parent.resolve()

MAPS = [
    {
        "name": "1. Prologo",
        "name_lat": 44.478,
        "name_lon": 11.291,
        "lat": [44.48785, 44.48832, 44.48859, 44.48799, 44.48756],
        "lon": [11.28835, 11.28849, 11.28945, 11.28968, 11.28941],
        "r": 255,
        "g": 0,
        "b": 0,
    },
    {
        "name": "2. Gauss Green",
        "name_lat": 44.473,
        "name_lon": 11.291,
        "lat": [44.49677, 44.49949, 44.49925, 44.49449],
        "lon": [11.29900, 11.30400, 11.30473, 11.30307],
        "r": 255,
        "g": 127,
        "b": 0,
    },
    {
        "name": "3. Proiezioni Artistiche",
        "name_lat": 44.468,
        "name_lon": 11.291,
        "lat": [44.51641, 44.51712, 44.51675, 44.51604],
        "lon": [11.29653, 11.29701, 11.29819, 11.29786],
        "r": 255,
        "g": 255,
        "b": 0,
    },
    {
        "name": "4. Level UP",
        "name_lat": 44.478,
        "name_lon": 11.318,
        "lat": [44.48481, 44.48517, 44.48249, 44.48263],
        "lon": [11.26796, 11.27155, 11.27154, 11.26948],
        "r": 0,
        "g": 255,
        "b": 0,
    },
    {
        "name": "5. Treno",
        "name_lat": 44.473,
        "name_lon": 11.318,
        "lat": [44.49284, 44.49535, 44.49773, 44.49754, 44.49604, 44.49280],
        "lon": [11.28362, 11.28461, 11.28638, 11.28665, 11.28540, 11.28395],
        "r": 0,
        "g": 127,
        "b": 0,
    },
    {
        "name": "6. Bologna Arcade",
        "name_lat": 44.468,
        "name_lon": 11.318,
        "lat": [44.49323, 44.49910, 44.49866, 44.49408, 44.49149, 44.49138],
        "lon": [11.33582, 11.33825, 11.34622, 11.35199, 11.34653, 11.33995],
        "r": 127,
        "g": 0,
        "b": 0,
    },
]

@app.route("/live_gps", methods=["POST"])
def get_live_gps_data():
    content = request.json
    tried_passcode = content["passcode"]
    found_teams = list(TEAMS.find({"passcode": tried_passcode}))
    if len(found_teams) == 0:
        return "Unknown passcode", 400
    if len(found_teams) > 1:
        return "To many TEAMS whit this passcode! WTF?", 400

    my_team = found_teams[0]

    if my_team["name"] == "Exploration Team":
        return "Not Allow to see this!", 400

    admin = my_team["admin"]
    if admin:
        gps = list(GPS.find({},
                            {"_id": 0, "gps_name": 1, "locations": 1}))

    else:
        gps = list(GPS.find({"question_gps": True},
                            {"_id": 0, "gps_name": 1, "locations": 1}))
    answer = []
    for i in range(len(gps)):
        answer.append({"gps_name": gps[i]["gps_name"], "last_location": gps[i]["locations"][-1]})
    return jsonify(answer), 200

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

@app.route("/questions", methods=["POST"])
def get_questions():
    content = request.json
    tried_passcode = str(content["passcode"])
    result = list(TEAMS.find({"passcode": tried_passcode}, {"_id": 0, "name": 1}))
    if len(result) == 0:
        return "Unknown Team", 400
    elif len(result) > 1:
        return "To many TEAMS whit this passcode! WTF?", 400
    else:
        if result[0]["name"] != "Exploration Team":
            questions = list(QUESTIONS.find({"question_id": {"$nin": ["-1", "-2"]}}, {"_id": 0}))
            return jsonify(questions), 200
        else:
            questions = list(QUESTIONS.find({"question_id": {"$in": ["-1", "-2"]}}, {"_id": 0}))
            print("Matching questions: {}".format(questions))
            return jsonify(questions), 200

@app.route("/maps", methods=["POST"])
def get_maps():
    content = request.json
    tried_passcode = str(content["passcode"])
    result = list(TEAMS.find({"passcode": tried_passcode}, {"_id": 0, "name": 1}))
    if len(result) == 0:
        return "Unknown Team", 400
    elif len(result) > 1:
        return "To many TEAMS whit this passcode! WTF?", 400
    else:
        if result[0]["name"] != "Exploration Team":
            return MAPS, 200
        else:
            return "Not allow to have this information!", 400

@app.route("/answers", methods=["POST"])
def get_answers():
    content = request.json
    tried_passcode = str(content["passcode"])
    result = list(TEAMS.find({"passcode": tried_passcode}, {"_id": 0, "answers": 1}))
    if len(result) == 0:
        response = {"team": "Unknown"}
        print("team unknown!")
    elif len(result) > 1:
        return "To many TEAMS whit this passcode! WTF?", 400
    else:
        response = result[0]["answers"]
    return jsonify(response)

@app.route('/photo_answers', methods=['POST'])
def get_image():
    content = request.json
    tried_passcode = str(content["passcode"])
    question_id = content["question_id"]
    result = list(TEAMS.find({"passcode": tried_passcode}, {"_id": 0, "answers": 1}))
    if len(result) == 0:
        response = {"team": "Unknown"}
        print("team unknown!")
    elif len(result) > 1:
        return "To many TEAMS whit this passcode! WTF?", 400
    else:
        response = result[0]["answers"]
    for resp in response:
        if resp["question_id"] == str(question_id):
            return send_file(resp["answer"][-1], mimetype='image/jpeg')
    return "Answer not found", 205

    # return send_file(file_path, mimetype='image/jpeg')


@app.route('/answer', methods=["POST"])
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


@app.route('/photo_upload', methods=['POST'])
def upload_a_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    c = datetime.now()
    current_time = c.strftime("%H:%M:%S.jpg")

    file_path = os.path.join(NUTBUS_FOLDER, "received_photo", current_time)
    file.save(file_path)
    hd_file_path = os.path.join(NUTBUS_FOLDER, "hd_received_photo", current_time)
    shutil.copyfile(file_path, hd_file_path)
    try:
        img = cv2.imread(file_path)
        scale_percent = 10

        # Calcola le nuove dimensioni
        width = int(200)
        height = int(img.shape[0] * (200/img.shape[1]))
        print(f"({width}x{height}) {img.shape}")
        dim = (width, height)

        # Ridimensiona l'immagine mantenendo le proporzioni
        resized_img = cv2.resize(img, dim)
        cv2.imwrite(file_path, resized_img)
    except Exception as e:
        print(e)
        return jsonify({'message': 'ERROR, probably not an IMAGE!'}), 400

    tried_passcode = str(request.form.get("passcode"))
    answer_id = str(request.form.get("question_id"))
    result = TEAMS.update_one(
        {"passcode": tried_passcode, "answers.question_id": answer_id},
        {"$push": {"answers.$.answer": file_path}}
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
                {"$push": {"answers": {"question_id": answer_id, "answer": [file_path]}}}
            )

    return jsonify({'message': 'File uploaded successfully'}), 200


if __name__ == '__main__':
    live_gps.thread.start()
    app.run(host="0.0.0.0", port=4999)


