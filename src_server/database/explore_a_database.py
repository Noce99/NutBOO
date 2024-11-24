from pymongo import MongoClient
# sudo systemctl start mongod.service

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')

    while True:
        all_database = client.list_database_names()
        print("@"*100)
        print("All Database List:")
        print(all_database)
        answer = input("Which database you want to explore? [q to quit] :")
        if answer == "q":
            exit()
        if answer not in all_database:
            print("Database not found try again!")
            continue
        my_database_name = answer
        db = client[my_database_name]
        while True:
            collections = db.list_collection_names()
            print("#" * 100)
            print(f"All collections in {my_database_name}:")
            for collection in collections:
                print(collection)
            answer = input("Which collection you want to explore? [q to quit, b to back] :")
            if answer == "q":
                exit()
            if answer == "b":
                break
            if answer not in collections:
                print("Collection not found try again!")
                continue
            my_collection_name = answer
            my_collection = db[my_collection_name]
            documents = my_collection.find()

            print("Alla documents:")
            for document in documents:
                print(document)