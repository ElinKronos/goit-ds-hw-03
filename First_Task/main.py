# Here begins a new World ...

import create_db

from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://ElinKronos44:Elin_4501612820@cluster0.cpgyzrh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db_name = "docs"
collection_name = "cats"

try:
    db_list = client.list_database_names()
    if db_name not in db_list:
        create_db.create_db()
except Exception as e:
    print(e)

def read_all_cats():
    db = client[db_name]
    cats = db[collection_name].find()
    for cat in cats:
        print(cat)

def find_cat():
    db = client[db_name]
    name = input("Введіть ім'я кота: ")
    cat = db[collection_name].find_one({"name": name})

    if cat:
        print(cat)
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

def update_cat_age():
    db = client[db_name]
    name = input("Введіть ім'я кота: ")
    new_age = int(input("Введіть новий вік кота: "))

    result = db[collection_name].update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )

    if result.matched_count == 0:
        print(f"Кота з ім'ям '{name}' не знайдено.")
    elif result.modified_count == 0:
        print(f"Вік уже дорівнює {new_age}, змін не внесено.")
    else:
        print(f"Вік кота '{name}' оновлено до {new_age}.")

def add_cat_feature():
    db = client[db_name]
    name = input("Введіть ім'я кота: ")
    new_feature = input("Введіть нову характеристику: ")

    result = db[collection_name].update_one(
        {"name": name},
        {"$addToSet": {"features": new_feature}}
    )

    if result.matched_count == 0:
        print(f"Кота з ім'ям '{name}' не знайдено.")
    elif result.modified_count == 0:
        print(f"Характеристика '{new_feature}' вже існує у кота '{name}'.")
    else:
        print(f"Коту '{name}' додано характеристику: {new_feature}.")

def delete_cat():
    db = client[db_name]
    name = input("Введіть ім'я кота: ")

    result = db[collection_name].delete_one({"name": name})

    if result.deleted_count > 0:
        print(f"Кіт '{name}' видалений.")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

def delete_all_cats():
    db = client[db_name]

    result = db[collection_name].delete_many({})

    print(f"Видалено {result.deleted_count} записів із колекції")



