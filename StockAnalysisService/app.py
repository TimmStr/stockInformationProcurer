import os

import requests
from flask import Flask, request, send_file
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint

from AnalysisService import start_analysis_for_ticker
from Path.paths import *
from Utils.messages import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True

# URL for Swagger UI
SWAGGER_URL = '/api/docs'
# Location of the swagger.json
API_URL = 'http://localhost:9030/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Stock Analysis Service"
    }
)

app.register_blueprint(swaggerui_blueprint)

ticker_parameter = api.model('Parameter', {
    'ticker': fields.String(required=True, description='Das Tickersymbol z.B. NASDAQ:AAPL')
})


@api.route('/mail')
class GetMail(Resource):
    def get(self):
        URL = MAIL_SERVICE + 'get'
        response = requests.get(URL)
        return response.content


@api.route('/startAnalysis')
class StartAnalysis(Resource):
    @api.expect(ticker_parameter)
    def get(self):
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


@api.route('/get_graphs')
class GetGraphs(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        ticker = request.values.get('ticker')
        date = request.values.get('date')
        file_name = GRAPHS + ticker + date + '.png'
        if request.values.get('period') is not None:
            period = request.values.get('period')
        if os.path.exists(file_name):
            return send_file(file_name)
        else:
            # ToDo Get Data from Database and create graphs
            return {"Muss noch eingefügt werden": True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
