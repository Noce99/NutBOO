from pymongo import MongoClient
# sudo systemctl start mongod.service

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    print("All Database List:")
    print(client.list_database_names())
