import requests
from bson.json_util import dumps
from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
print('version 6')

#test
@app.route('/get', methods=['GET'])
def get_test():
    return 'Successful'


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


@app.route('/testdocument', methods=['GET'])
def test_document():
    BASE_URL = 'http://stockinformationprocurer-document-service-1:9010'
    URL = BASE_URL + '/get'
    response = requests.get(URL)
    print(response)
    print(response.content)
    return response.content


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
