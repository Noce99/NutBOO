from pymongo import MongoClient
# sudo systemctl start mongod.service

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["boo2024"]
    TEAMS = db["teams"]
    QUESTIONS = db["questions"]
    GPS = db["gps"]

    questions = list(QUESTIONS.find({}, {"_id": 0}))
    print(questions)

