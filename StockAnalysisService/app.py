import requests
import os
from bson.json_util import dumps
from flask import Flask, request, send_file
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

@app.route('/get_all_data_entries', methods=['GET'])
def get_all_data_entries():
    entries = collection.find()
    entries_as_json = dumps(entries)
    return entries_as_json


def delete_collection_entries():
    collection.delete_many({})


@app.route('/get_data_for/<string:symbol>', methods=['GET'])
def get_data_for_symbol(symbol):
    ### hier kommt Code zum ziehen aus der Datenbank
    # delete_collection_entries()

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

    return dumps(dicts)


def read_data_from_csv(symbol='TSLA'):
    with open('TSLA.csv', 'r') as file:
        return file.readlines()


@app.route('/startAnalysis', methods=['GET'])
def start_analysis():
    return start_analysis_for_symbol(collection)


@app.route('/get_graphs', methods=['GET'])
def get_graphs():
    symbol = request.values.get('symbol')
    date = request.values.get('date')
    file_name = symbol+date+'.png'
    if request.values.get('period') is not None:
        period = request.values.get('period')
    if os.path.exists(file_name):
        return send_file(file_name)
    else:
        #ToDo Get Data from Database and create graphs
        return {"Muss noch eingefügt werden": True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))