import os

import requests
from flask import Flask, request, send_file
from flask_restful import Api

from AnalysisService import start_analysis_for_ticker
from Path.paths import *
from Utils.messages import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True


stock_scraping_service = STOCK_WEB_SCRAPING_SERVICE


@app.route('/mail', methods=['GET'])
def test_mail():
    URL = MAIL_SERVICE + 'get'
    response = requests.get(URL)
    return response.content


@app.route('/startAnalysis', methods=['GET'])
def start_analysis():
    request_values = request.values

    if request_values.get('ticker') is not None:
        try:
            stock_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_STOCK_FROM_TICKER,
                                          params=request_values.to_dict())
            stocks = stock_response.content

            # ToDo StockWebScrapingService muss umgebaut werden. Insbesonder gspread_scraper (jsonify)??? oder gleich als worksheet?
            print(stocks)
            print(type(stocks))
            print(type(stocks.keys))
            print(type(stocks.values))
            kpi_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_KPIS_FROM_TICKER,
                                        params=request_values.to_dict())
            kpis = kpi_response.content
            print(kpis)
            start_analysis_for_ticker(stocks["Ticker"], stocks["Stocks"])
            return stock_response
        except:
            return ERROR_OCCURED
    else:
        return PASS_A_TICKERSYMBOL


@app.route('/get_graphs', methods=['GET'])
def get_graphs():
    symbol = request.values.get('symbol')
    date = request.values.get('date')
    file_name = GRAPHS + symbol + date + '.png'
    if request.values.get('period') is not None:
        period = request.values.get('period')
    if os.path.exists(file_name):
        return send_file(file_name)
    else:
        # ToDo Get Data from Database and create graphs
        return {"Muss noch eingefügt werden": True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
