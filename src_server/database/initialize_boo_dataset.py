from pymongo import MongoClient
# sudo systemctl start mongod.service

YEAR = "2024"

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    all_database = client.list_database_names()
    if f"boo{YEAR}" in all_database:
        answer = input(f"boo{YEAR} dataset already present! Do you want to delete it and create it as new? (y/n)")
        if answer != "y":
            exit()
        client.drop_database(f"boo{YEAR}")

    db = client[f"boo{YEAR}"]
    # TEAMS
    teams_collection = db["teams"]

    admin = {
        "name": "Admin",
        "passcode": "svettavento",
        "admin": True,
        "answers": [{"question_id": -2, "answer": "10"}, {"question_id": -1, "answer": "/home/enrico/Images/bho.jpg"},],
    }

    test_team = {
        "name": "Team 1",
        "passcode": "hobbit",
        "admin": False,
        "answers": []
    }

    teams_collection.insert_one(admin)
    teams_collection.insert_one(test_team)

    # PRINT TEAMS
    documents = teams_collection.find()

    print("TEAMS:")
    for document in documents:
        print(document)

    # QUESTIONS
    questions_collection = db["questions"]

    test_test_question = {
        "question_id": -2,
        "question": "How many l in Marcello?",
        "answer": "2",
        "answer_type": "text"
    }

    test_image_question = {
        "question_id": -1,
        "question": "An amazing picture!",
        "answer": "NO CORRECT ANSWER TO PICTURES",
        "answer_type": "image"
    }

    questions_collection.insert_one(test_test_question)
    questions_collection.insert_one(test_image_question)

    # PRINT QUESTIONS
    documents = questions_collection.find()

    print("QUESTIONS:")
    for document in documents:
        print(document)

    # LIVE GPS
    gps_collection = db["gps"]

    question_gps = {
        "question_gps": True,
        "gps_id": "-1",
        "location": [{"time": 100, "lat": 0.0, "lon": 0.0}],
        "gps_name": "Marci with a Bicycle"
    }

    team_gps = {
        "question_gps": False,
        "gps_id": "-2",
        "location": [{"time": 300, "lat": 0.0, "lon": 0.0}, {"time": 400, "lat": 44.0, "lon": 0.0}],
        "gps_name": "Team 1"
    }

    gps_collection.insert_one(question_gps)
    gps_collection.insert_one(team_gps)

    # PRINT QUESTIONS
    documents = gps_collection.find()

    print("GPS:")
    for document in documents:
        print(document)





