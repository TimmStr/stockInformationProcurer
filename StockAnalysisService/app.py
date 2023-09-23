"""
Builds a Flask app that runs the StockAnalysisService in a docker container.
The restx-Endpoints are been defined here via annotations as this is recommended by the Flask framework.
The StockAnalysisService can be seen as the main entrypoint to the application as this service is pulling data through
the other services and handles the main functions, e.g. analyzing stocks and drawing plots.
So this service is an important part of the architecture of this application.
"""

import os

from flask import Flask, request, send_file
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
from AnalysisService import start_analysis_for_ticker
from Utils.paths import *
from Utils.messages import *
from Service.GetInformationService import *
from Service.AuthenticationService import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True


"""
Swagger config. The json file is available at "http://localhost:9030/swagger.json" while the official Swagger UI URL
is available under "http://localhost:9030/api/docs/".
"""
SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:9030/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Stock Analysis Service"
    }
)
app.register_blueprint(swaggerui_blueprint)


"""
Defines the parameter that are required for some functions.
Example: The data for a stock cannot be pulled, if there is no symbol given. 
"""
ticker_parameter = api.model('Parameter', {
    'ticker': fields.String(required=True, description='The Tickersymbol is missing. Example: {"ticker":"NASDAQ:AAPL"}')
})

file_name = api.model('Parameter', {
    'file_name': fields.String(required=True, description='Filename')
})


"""
Creating the path for saving the plots if it does not exist .
"""
if not os.path.exists('Graphs'):
    os.makedirs('Graphs')


# Endpoint to pull data from the database returns all data
@api.route('/getStocksFromDatabase')
class GetStocksFromDatabase(Resource):
    def get(self):
        """
        Retrieves all stocks from WebScrapingService.
        :return:
            if authentication successful: Json response from WebScrapingService with all the stocks
            else: Message which tells that the authentication was not successful.
        """
        if authenticate_user(request.values):
            return get_all_stocks_from_database()
        else:
            return AUTHENTICATION_FAILED


# Endpoint to pull data from the database returns data for a given ticker (specific stock)
@api.route('/getStockFromDatabase')
class GetStockFromDatabase(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        """
        Gets stocks for a given ticker (specific stock)
        :return:
            if authentication was successful:
                if ticker is not Null/None:
                    if get request from Database was successful:
                        Json answer from WebScrapingService with the stocks for the given ticker
                    else:
                        {"Successful": False, "Error": Exception}
                else:
                    Str: "Please pass a tickersymbol. Example: {"ticker": "NASDAQ:GOOGL"}."
            else: "Authentication failed. {"mail":"xyz", "password": "1234"}"
        """
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


# Endpoint to call the analysis function
@api.route('/startAnalysis')
class StartAnalysis(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        """
        Starts analysis for a given ticker
        :return:
            if authentication was successful:
                if ticker is not Null/None:
                    if get request from Database was successful:
                        dict with values like min, max and the filenames for the graphs
                    else:
                        {"Successful": False, "Error": Exception}
                else:
                    Str: "Please pass a tickersymbol. Example: {"ticker": "NASDAQ:GOOGL"}."
            else: "Authentication failed. {"mail":"xyz", "password": "1234"}"
        """
        if authenticate_user(request.values):
            request_values = request.values
            if request_values.get('ticker') is not None:
                try:
                    stock_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_STOCK_FROM_TICKER,
                                                  params=request_values.to_dict())
                    stocks = stock_response.json()
                    return start_analysis_for_ticker(stocks["Ticker"], stocks["Stocks"], request_values)
                except Exception as e:
                    return {"Succesful": False, "Error": str(e)}
            else:
                return PASS_A_TICKERSYMBOL
        return AUTHENTICATION_FAILED


# Endpoint for deleting the png files
@api.route('/deleteFiles')
class DeleteFiles(Resource):
    @api.expect(file_name)
    def get(self):
        """
        Function for deleting the png Files.
        :return:
            if authentication successful:
                if remove successful:
                    {"Succesful deleted": "True"}
                else:
                    {"Succesful": False, "Error": Exception}
            else: Message which tells that the authentication was not successful.
        """
        if authenticate_user(request.values):
            try:
                os.remove(file_name)
                return {"Succesful deleted": "True"}
            except Exception as e:
                return {"Succesful": False, "Error": str(e)}
        else:
            return AUTHENTICATION_FAILED


# Endpoint for returning the graph as png
@api.route('/getGraphs')
class GetGraphs(Resource):
    @api.expect(file_name)
    def get(self):
        """
        Returns a graph as png
        :return:
            if authentication was successful:
                if filename is not null/none:
                    if path on server is not null/none:
                        return png file
                    else:
                        {"Successful": False, "Error": Exception}
                else:
                    Str: "Please pass a tickersymbol. Example: {"ticker": "NASDAQ:GOOGL"}."
            else: "Authentication failed. {"mail":"xyz", "password": "1234"}"
        """
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
