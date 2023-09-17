from flask import Flask, request
from flask_restful import Api

from MongoDb.MongoService import *
from Scraper.gspread_scraper import *
from Utils.messages import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True


@app.route('/get_stock_from_ticker', methods=['GET'])
def get_stock_from_ticker():
    if request.values.get('ticker') is not None:
        try:
            return {"Ticker": request.values.get('ticker'),
                    "Stocks": get_stock_data_as_json(request.values.get('ticker'))}
        except:
            return ERROR_OCCURED
    else:
        return PASS_A_TICKERSYMBOL

@app.route('/get_kpis_from_ticker', methods=['GET'])
def get_kpis_from_ticker():
    if request.values.get('ticker') is not None:
        try:
            return {"KPIs": get_kpis_as_dict(request.values.get('ticker'))}
        except:
            return ERROR_OCCURED
    else:
        return PASS_A_TICKERSYMBOL

@app.route('/save_stock', methods=['GET'])
def save_stock():
    if request.values.get('ticker') is not None:
        try:
            data_dicts = get_stock_data_as_list_of_dicts(request.values.get('ticker'))
            return save_data_dicts(data_dicts)
        except:
            return ERROR_OCCURED
    else:
        return PASS_A_TICKERSYMBOL


@app.route('/get_all_stocks', methods=['GET'])
def get_all_stocks():
    try:
        return get_all_stocks_from_mongo_db()
    except:
        return ERROR_OCCURED


@app.route('/delete_all_stocks', methods=['GET'])
def delete_all_stocks():
    try:
        delete_all_stocks_from_mongo_db()
        return STOCKS_DELETED
    except:
        return ERROR_OCCURED


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
