import os

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/get', methods=['GET'])
def get_test():
    return 'Successful'


@app.route('/testmongo', methods=['GET'])
def test_mongo():
    # Verbindung zur MongoDB-Datenbank herstellen
    client = MongoClient("mongodb://localhost:27017/")
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
        collection.insert_one(entry)

    return "Daten erfolgreich eingefügt."


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
