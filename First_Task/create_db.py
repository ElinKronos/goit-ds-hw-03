
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://ElinKronos44:Elin_4501612820@cluster0.cpgyzrh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

def create_db():
    db_name = "docs"
    collection_name = "cats"

    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(
        {
            "name": "name",
            "age": 0,
            "features": ["feature_1", "feature_2", "feature_3"],
        }
    )
    print("Database created successfully")

if __name__ == "__main__":
    create_db()

