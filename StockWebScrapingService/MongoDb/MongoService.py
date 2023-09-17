from bson.json_util import dumps
from pymongo import MongoClient

from Utils.paths import *

client = MongoClient(MONGO_PATH)
db = client[MONGO_CLIENT]
collection = db[MONGO_DATABASE]


def save_data_dicts(list_of_dicts):
    collection.insert_many(list_of_dicts)
    return "Stocks inserted"


def save_data_dict(dict):
    return collection.insert_one(dict)


def get_all_stocks_from_mongo_db():
    entries = collection.find()
    return dumps(entries)
#ToDo Get-Funktion für einzelne Stocks


def delete_all_stocks_from_mongo_db():
    return collection.delete_many({})
