import requests
from bson.json_util import dumps
from flask import Flask, request
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
mailserver = "http://stockinformationprocurer-mail-service-1:9020"


@app.route('/mail', methods=['GET'])
def test_mail():
    URL = mailserver + '/get'
    response = requests.get(URL)
    return response.content


@app.route('/testmongo_upload', methods=['GET'])
def test_mongo_upload():
    # Verbindung zur MongoDB-Datenbank herstellen
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["stockinformations"]

    collection = db["stocks"]

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
    # Verbindung zur MongoDB-Datenbank herstellen
    # client = MongoClient("mongodb://mongodb/")
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["stockinformations"]

    collection = db["stocks"]
    entries = collection.find()
    entries_as_json = dumps(entries)
    return entries_as_json


@app.route('/get_data_for/<string:symbol>', methods=['GET'])
def get_data_for_symbol(symbol):
    ### hier kommt Code zum ziehen aus der Datenbank

    data = read_data_from_csv()
    return data


def read_data_from_csv(symbol='TSLA'):
    with open('TSLA.csv', 'r') as file:
        return file.readlines()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
