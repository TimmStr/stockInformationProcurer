"""
This file includes many functions to communicate with the mongo database.
"""

from bson.json_util import dumps
from pymongo import MongoClient
from Scraper.gspread_scraper import *
from Utils.paths import *

client = MongoClient(MONGO_PATH)
db = client[MONGO_CLIENT]
collection = db[MONGO_DATABASE]


def save_data_dicts(list_of_dicts):
    """
    Stores multiple dictionaries in one go in the mongo database.
    :param list_of_dicts:
    :return:
        str
    """
    collection.insert_many(list_of_dicts)
    return "Stocks inserted"


def save_stock_in_database(ticker):
    """
    Saves stock in mongo database.
    It checks if the entry is already included. If not, it will be inserted now.
    If every entry is already included, there won't be any insertions.
    :param ticker:
    :return:
        dict
    """
    data_dicts = get_stock_data_as_list_of_dicts(ticker)
    inserted_count = 0
    for dicti in data_dicts:
        existing_entry = find_one({"Ticker": ticker, "Date": dicti["Date"]})

        if not existing_entry:
            save_data_dict(dicti)
            inserted_count += 1
    if inserted_count > 0:
        return {"Successful": True, "InsertedCount": inserted_count}
    else:
        return {"Successful": True, "Message": "Alle Daten waren bereits vorhanden."}


def save_data_dict(dict):
    """
    Stores dict in mongo database.
    :param dict: dict
    :return:
        ObjectId
    """
    return collection.insert_one(dict)


def find_one(dict):
    """
    Finds a entry in mongo database.
    :param dict: dict
    :return:
        dict
    """
    return collection.find_one(dict)


def get_all_stocks_from_mongo_db():
    """
    Finds and returns all mongo database entries.
    :return:
        dict
    """
    entries = collection.find()
    return dumps(entries)


def get_stock_from_mongo_db(ticker):
    """
    Finds all mongo database entries with a specific tickersymbol. E.g. {"Ticker":"NASDAQ:NVDA"}
    If the tickersymbol is not yet in the database, it will be stored now.
    :param ticker:
    :return:
    """
    query = {"Ticker": ticker}
    entries = collection.find(query)
    as_dict = [entry for entry in entries]
    if len(as_dict) > 0:
        return dumps(as_dict)
    else:
        save_stock_in_database(ticker)
        get_stock_from_mongo_db(ticker)


def delete_all_stocks_from_mongo_db():
    """
    Deletes all mongo database entries.
    """
    return collection.delete_many({})
