from bson.json_util import dumps
from pymongo import MongoClient
from Scraper.gspread_scraper import *
from Utils.paths import *

client = MongoClient(MONGO_PATH)
db = client[MONGO_CLIENT]
collection = db[MONGO_DATABASE]


def save_data_dicts(list_of_dicts):
    collection.insert_many(list_of_dicts)
    return "Stocks inserted"


def save_stock_in_database(ticker):
    data_dicts = get_stock_data_as_list_of_dicts(ticker)
    inserted_count = 0
    for dicti in data_dicts:
        existing_entry = find_one({"Ticker": ticker, "Date": dicti["Date"]})

        if not existing_entry:
            save_data_dict(dicti)
            inserted_count += 1
    if inserted_count > 0:
        return {"Succesful": True, "InsertedCount": inserted_count}
    else:
        return {"Succesful": True, "Message": "Alle Daten waren bereits vorhanden."}


def save_data_dict(dict):
    return collection.insert_one(dict)


def find_one(dict):
    return collection.find_one(dict)


def get_all_stocks_from_mongo_db():
    entries = collection.find()
    return dumps(entries)


# ToDo Get-Funktion für einzelne Stocks

def get_stock_from_mongo_db(ticker):
    query = {"Ticker": ticker}
    entries = collection.find(query)
    as_dict = [entry for entry in entries]
    if len(as_dict) > 0:
        return dumps(as_dict)
    else:
        save_stock_in_database(ticker)
        get_stock_from_mongo_db(ticker)


def delete_all_stocks_from_mongo_db():
    return collection.delete_many({})
