import requests
from bson.json_util import dumps
from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

from AnalysisService import start_analysis_for_symbol
from Path.paths import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

mailserver = MAIL_SERVICE
client = MongoClient(MONGO_PATH)
db = client[MONGO_CLIENT]
collection = db[MONGO_DATABASE]


@app.route('/mail', methods=['GET'])
def test_mail():
    URL = mailserver + '/get'
    response = requests.get(URL)
    return response.content


@app.route('/testmongo_upload', methods=['GET'])
def test_mongo_upload():
    # Beispiel-Daten zum Einfügen
    data_to_insert = [
        {"symbol": "AAPL", "price": 150.25, "volume": 200},
        {"symbol": "GOOGL", "price": 2800.50, "volume": 800},
        {"symbol": "AMZN", "price": 3500.75, "volume": 950}
    ]

    # Daten in die Datenbank einfügen
    for entry in data_to_insert:
        print(entry)
        collection.insert_one(entry)

    return "Daten erfolgreich eingefügt."


@app.route('/testmongo_get', methods=['GET'])
def test_mongo_get():
    print('Get Test:')
    entries = collection.find()
    entries_as_json = dumps(entries)
    return entries_as_json


def delete_collection_entries():
    collection.delete_many({})


@app.route('/get_data_for/<string:symbol>', methods=['GET'])
def get_data_for_symbol(symbol):
    ### hier kommt Code zum ziehen aus der Datenbank
    # delete_collection_entries()

    print('Hello')
    data = read_data_from_csv()
    columns = data[0]

    print("Columns", columns)

    entries = [entry.strip("\n") for entry in data[1:]]
    dicts = []
    for entry in entries:
        splitted_entry = entry.split(',')
        # print(splitted_entry)
        date = splitted_entry[0]
        open = splitted_entry[1]
        high = splitted_entry[2]
        low = splitted_entry[3]
        close = splitted_entry[4]
        volume = splitted_entry[6]
        data_dict = {
            'Symbol': symbol,
            'Date': date,
            'Open': open,
            'High': high,
            'Low': low,
            'Close': close,
            'Volume': volume,
        }
        dicts.append(data_dict)
        print('Data Dict:')
        print(data_dict)
        # print(dumps(data_dict))
    result = collection.insert_many(dicts)
    # print(result.inserted_id)

    return entries


def read_data_from_csv(symbol='TSLA'):
    with open('TSLA.csv', 'r') as file:
        return file.readlines()


@app.route('/startAnalysis', methods=['GET'])
def start_analysis():
    return start_analysis_for_symbol(collection)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
