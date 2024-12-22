from pymongo import MongoClient
from boo2024_initialization import BOO2024_INITIALIZATION, initialize_a_team
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
        "answers": [{"question_id": "-2", "answer": ["10"]},
                    {"question_id": "-1", "answer": ["/home/enrico/Images/bho.jpg"]},],
    }

    teams = []
    teams.append(initialize_a_team("Noce", "hobbit"))
    teams.append(initialize_a_team("Seba", "bilbo"))

    teams.append(initialize_a_team("Boh", "36tagliatelle"))
    teams.append(initialize_a_team("BubuLoser", "36lasagne"))
    teams.append(initialize_a_team("Bus Brothers", "36tortellini"))
    teams.append(initialize_a_team("dis-ederati", "36passatelli"))
    teams.append(initialize_a_team("EAE from Gatta", "36pappardelle"))
    teams.append(initialize_a_team("Euforia", "36balanzoni"))
    teams.append(initialize_a_team("Free walking team", "36fusilli"))
    teams.append(initialize_a_team("Già lo sai", "36penne"))
    teams.append(initialize_a_team("Gli Amici dello Scaldaletto", "36farfalle"))
    teams.append(initialize_a_team("Gli sBOOssolati", "36rigatoni"))
    teams.append(initialize_a_team("I Bradipi", "36spaghetti"))
    teams.append(initialize_a_team("I cicis", "36bucatini"))
    teams.append(initialize_a_team("I Padri Pellegrini (BOOmer)", "36piadine"))
    teams.append(initialize_a_team("I salami piacentini", "36tigelle"))
    teams.append(initialize_a_team("I Tromboni di Naim", "36crescentine"))
    teams.append(initialize_a_team("I vagabondi", "36orecchiette"))
    teams.append(initialize_a_team("La Crisi è al Top", "36cannelloni"))
    teams.append(initialize_a_team("LaGangFiorentina", "36sedanini"))
    teams.append(initialize_a_team("Lantern Hunters", "36polpette"))
    teams.append(initialize_a_team("Le acquatrix", "36ravioli"))
    teams.append(initialize_a_team("Le Strane", "36pagnotte"))
    teams.append(initialize_a_team("M&M&M", "36canederli"))
    teams.append(initialize_a_team("Mailovini", "36pizzoccheri"))
    teams.append(initialize_a_team("Mammannapapalo", "36panigacci"))
    teams.append(initialize_a_team("non ci resta che piangere", "36borlenghi"))
    teams.append(initialize_a_team("Orientisti Americani", "36sfrappole"))
    teams.append(initialize_a_team("Paradise", "36farinate"))
    teams.append(initialize_a_team("Pia e Nino", "36brioche"))
    teams.append(initialize_a_team("Potrebbe andare peggio", "36castagnacci"))
    teams.append(initialize_a_team("sANTA polENTA", "36linguine"))
    teams.append(initialize_a_team("TOP TEAM (the last dance)", "36muffin"))
    teams.append(initialize_a_team("tt le girlz", "36crepes"))
    teams.append(initialize_a_team("WakeMeUp", "36biscotti"))
    teams.append(initialize_a_team("BUONA CACCIA", "36polenta"))

    teams.append(initialize_a_team("Cuscinetto1", "36torrone"))
    teams.append(initialize_a_team("Cuscinetto2", "36caramelle"))
    teams.append(initialize_a_team("Cuscinetto3", "36liquirizia"))


    exploration_team = {
        "name": "Test",
        "passcode": "test",
        "admin": False,
        "answers": []
    }

    teams_collection.insert_one(admin)
    for team in teams:
        teams_collection.insert_one(team)
    teams_collection.insert_one(exploration_team)

    # PRINT TEAMS
    documents = teams_collection.find()

    print("TEAMS:")
    for document in documents:
        print(document)

    # QUESTIONS
    questions_collection = db["questions"]

    test_test_question = {
        "question_id": "-2",
        "question": "Qui puoi rispondere ad una domanda di prova: Quante \"l\" ci sono in Marcello?",
        "answer": "2",
        "type_of_answer": "text"
    }

    test_image_question = {
        "question_id": "-1",
        "question": "Qui puoi provare a caricare una foto!",
        "answer": "NO CORRECT ANSWER TO PICTURES",
        "type_of_answer": "photo"
    }

    questions_collection.insert_one(test_test_question)
    questions_collection.insert_one(test_image_question)

    for el in BOO2024_INITIALIZATION:
        questions_collection.insert_one(el)

    # PRINT QUESTIONS
    documents = questions_collection.find()

    print("QUESTIONS:")
    for document in documents:
        print(document)

    # LIVE GPS
    gps_collection = db["gps"]

    question_gps = {
        "question_gps": True,
        "gps_id": "265885926911886639633859492011259188", #L605
        "locations": [{"time": 1732573084.0, "lat": 44.49632479573085, "lon": 11.321860276019171}],
        "gps_name": "Bonus 1"
    }

    team_gps = {
        "question_gps": True,
        "gps_id": "265885926911886639633859509275407414", # L257
        "locations": [{"time": 1732573084.0, "lat": 44.498222479680344, "lon": 11.34731287754418}],
        "gps_name": "Bonus 2"
    }

    gps_collection.insert_one(question_gps)
    gps_collection.insert_one(team_gps)

    # PRINT QUESTIONS
    documents = gps_collection.find()

    print("GPS:")
    for document in documents:
        print(document)





