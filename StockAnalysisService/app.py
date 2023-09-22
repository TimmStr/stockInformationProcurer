import os

import requests as rq
from flask import Flask, request, send_file, jsonify
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
import json
from AnalysisService import start_analysis_for_ticker
from Path.paths import *
from Utils.messages import *
from Service.GetInformationService import *
from Service.AuthenticationService import *

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

if not os.path.exists('Graphs'):
    os.makedirs('Graphs')


@api.route('/testAuth')
class TestAuth(Resource):
    def get(self):
        if authenticate_user(request.values):
            request_values = request.values
            print(request_values)
            return 'xy'
        else:
            return AUTHENTICATION_FAILED


@api.route('/getStocksFromDatabase')
class GetStocksFromDatabase(Resource):
    def get(self):
        if authenticate_user(request.values):
            print(get_all_stocks_from_database())
            return get_all_stocks_from_database()
        else:
            return AUTHENTICATION_FAILED


@api.route('/getStockFromDatabase')
class GetStockFromDatabase(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        if authenticate_user(request.values):
            request_values = request.values
            if request.values.get('ticker') is not None:
                try:
                    return stock_from_database(request_values.to_dict())
                except Exception as e:
                    return {"Succesful": False, "Error": str(e)}
            else:
                return PASS_A_TICKERSYMBOL
        return AUTHENTICATION_FAILED


@api.route('/startAnalysis')
class StartAnalysis(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        if authenticate_user(request.values):
            request_values = request.values
            if request_values.get('ticker') is not None:
                try:
                    stock_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_STOCK_FROM_TICKER,
                                                  params=request_values.to_dict())
                    stocks = stock_response.json()
                    print('Analysis',start_analysis_for_ticker(stocks["Ticker"], stocks["Stocks"]))
                    return start_analysis_for_ticker(stocks["Ticker"], stocks["Stocks"])
                except Exception as e:
                    return {"Succesful": False, "Error": str(e)}
            else:
                return PASS_A_TICKERSYMBOL
        return AUTHENTICATION_FAILED


# @api.route('/startAnalysis')
# class GetKpis(Resource):
#     @api.expect(ticker_parameter)
#     def get(self):
#         if authenticate_user(request.values):
#             request_values = request.values
#             if request_values.get('ticker') is not None:
#                 try:
#                     kpi_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_KPIS_FROM_TICKER,
#                                                 params=request_values.to_dict())
#                     return kpi_response.json()
#                 except Exception as e:
#                     return {"Succesful": False, "Error": str(e)}
#             else:
#                 return PASS_A_TICKERSYMBOL
#         return AUTHENTICATION_FAILED


@api.route('/getGraphs')
class GetGraphs(Resource):
    @api.expect(file_name)
    def get(self):
        if authenticate_user(request.values):
            if request.values.get('file_name') is not None:
                file_name = request.values.get('file_name')
                try:
                    if os.path.exists(file_name):
                        return send_file(file_name)
                except Exception as e:
                    return {"Succesful": False, "Error": str(e)}
            else:
                return PASS_A_FILENAME
        return AUTHENTICATION_FAILED


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
