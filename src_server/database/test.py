from pymongo import MongoClient
# sudo systemctl start mongod.service

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["boo2024"]
    TEAMS = db["teams"]
    QUESTIONS = db["questions"]
    GPS = db["gps"]

    found_gps = list(GPS.find({"gps_id": "-2"}))
    my_gps = found_gps[0]
    last_position = my_gps["location"][-1]

    print(my_gps)
    print(last_position)

