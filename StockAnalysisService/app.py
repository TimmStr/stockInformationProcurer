import os

import requests
from flask import Flask, request, send_file
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
import json
from AnalysisService import start_analysis_for_ticker
from Path.paths import *
from Utils.messages import *
from Service.GetInformationService import *

"""
Builds a Flask app that runs a service in a docker container. The RESTful-Endpoints are been defined here via annotations as
this is recommended by the Flask framework. The StockAnalysisService can be seen as the main entrypoint to the application as
this service is pulling data through the other services and handles the main functions, e.g. StockAnalysis and drawing of plots.
So this service is an important part of the architecture of this application.
"""

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

file_name = api.model('Parameter', {
    'file_name': fields.String(required=True, description='Filename')
})

# Endpoint for mail service
@api.route('/mail')
class GetMail(Resource):
    def get(self):
        URL = MAIL_SERVICE + 'get'
        response = requests.get(URL)
        return response.json()

# Endpoint to pull data from the database returns all data
@api.route('/getStocksFromDatabase')
class GetStocksFromDatabase(Resource):
    def get(self):
        print(get_all_stocks_from_database())
        return get_all_stocks_from_database()

# Endpoint to pull data from the database returns data for a given ticker (specific stock)
@api.route('/getStockFromDatabase')
class GetStockFromDatabase(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        request_values = request.values
        if request.values.get('ticker') is not None:
            try:
                return stock_from_database(request_values.to_dict())
            except Exception as e:
                return {"Succesful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL

# Endpoint to call the analysis function
@api.route('/startAnalysis')
class StartAnalysis(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        request_values = request.values
        if request_values.get('ticker') is not None:
            try:
                stock_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_STOCK_FROM_TICKER,
                                              params=request_values.to_dict())
                stocks = stock_response.json()
                # print(stocks["Ticker"])
                # print(stocks["Stocks"])

                # ToDo StockWebScrapingService muss umgebaut werden. Insbesonder gspread_scraper (jsonify)??? oder gleich als worksheet?
                # kpi_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_KPIS_FROM_TICKER,
                #                             params=request_values.to_dict())
                # kpis = kpi_response.json()

                return start_analysis_for_ticker(stocks["Ticker"], stocks["Stocks"])
            except Exception as e:
                return {"Succesful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL

# Endpoint to call the analysis function
@api.route('/startAnalysis')
class GetKpis(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        request_values = request.values
        if request_values.get('ticker') is not None:
            try:
                kpi_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_KPIS_FROM_TICKER,
                                            params=request_values.to_dict())
                return kpi_response.json()
            except Exception as e:
                return {"Succesful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL

# # Endpoint to call the plot function
@api.route('/getGraphs')
class GetGraphs(Resource):
    @api.expect(file_name)
    def get(self):
        if request.values.get('file_name') is not None:
            file_name = request.values.get('file_name')
            try:
                if os.path.exists(file_name):
                    return send_file(file_name)
            except Exception as e:
                return {"Succesful": False, "Error": str(e)}
        else:
            return PASS_A_FILENAME


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
