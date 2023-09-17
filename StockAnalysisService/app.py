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

mailserver = MAIL_SERVICE
stock_scraping_service = STOCK_WEB_SCRAPING_SERVICE


@app.route('/mail', methods=['GET'])
def test_mail():
    URL = mailserver + '/get'
    response = requests.get(URL)
    return response.content

@app.route('/startAnalysis', methods=['GET'])
def start_analysis():
    if request.values.get('ticker') is not None:
        try:
            response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_STOCK_FROM_TICKER + request.values.get('ticker'))
            data = response.content
            start_analysis_for_ticker(data.get("Ticker"), data.get("Stocks"))
            return response
        except:
            return ERROR_OCCURED
    else:
        return PASS_A_TICKERSYMBOL



@app.route('/get_graphs', methods=['GET'])
def get_graphs():
    symbol = request.values.get('symbol')
    date = request.values.get('date')
    file_name = symbol + date + '.png'
    if request.values.get('period') is not None:
        period = request.values.get('period')
    if os.path.exists(file_name):
        return send_file(file_name)
    else:
        # ToDo Get Data from Database and create graphs
        return {"Muss noch eingefügt werden": True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
