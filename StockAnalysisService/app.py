"""
Builds a Flask app that runs the StockAnalysisService in a docker container.
The restx-Endpoints are been defined here via annotations as this is recommended by the Flask framework.
The StockAnalysisService can be seen as the main entrypoint to the application as this service is pulling data through
the other services and handles the main functions, e.g. analyzing stocks and drawing plots.
So this service is an important part of the architecture of this application.
"""

import os

from flask import Flask, request, send_file
from flask_restx import Api, Resource, fields, reqparse
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
Defines the parameter that are required for the get function.
Example: The data for a stock cannot be pulled, if there is no symbol given. 
"""
start_analysis_parser = reqparse.RequestParser()
start_analysis_parser.add_argument('ticker', type=str, required=True,
                                   help='The Tickersymbol is missing. Example: {"ticker":"NASDAQ:AAPL"}')
start_analysis_parser.add_argument('mail', type=str, required=True, help='The email address for the user is missing.')
start_analysis_parser.add_argument('password', type=str, required=True, help='The password for the user is missing.')
start_analysis_parser.add_argument('start_date', type=str, required=False,
                                   help='Start date represents the beginning of the analysis. E.g. 12-08-2023. If not specified, the default value is used (One year ago).')
start_analysis_parser.add_argument('end_date', type=str, required=False,
                                   help='End date represents the beginning of the analysis. E.g. 25-09-2023. If not specified, the default value is used (today)')

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('mail', type=str, required=True, help='The email address for the user is missing.')
auth_parser.add_argument('password', type=str, required=True, help='The password for the user is missing.')

auth_and_ticker_parser =reqparse.RequestParser()
auth_and_ticker_parser.add_argument('ticker', type=str, required=True,
                                   help='The Tickersymbol is missing. Example: {"ticker":"NASDAQ:AAPL"}')
auth_and_ticker_parser.add_argument('mail', type=str, required=True, help='The email address for the user is missing.')
auth_and_ticker_parser.add_argument('password', type=str, required=True, help='The password for the user is missing.')

auth_and_file_parser = reqparse.RequestParser()
auth_and_file_parser.add_argument('file_name', type=str, required=True,
                                   help='The file_name is missing.')
auth_and_file_parser.add_argument('mail', type=str, required=True, help='The email address for the user is missing.')
auth_and_file_parser.add_argument('password', type=str, required=True, help='The password for the user is missing.')

"""
Defines the parameter for the Swagger UI.
"""
start_analysis_parameters = api.model('Parameters for Start Analysis', {
    'ticker': fields.String(required=True,
                            description='The Tickersymbol is missing. Example: {"ticker":"NASDAQ:AAPL"}'),
    'mail': fields.String(required=True,
                          description='The email address for the user is missing.'),
    'password': fields.String(required=True,
                              description='The password for the user is missing.'),
    'start_date': fields.String(required=False,
                                description='Start date represents the beginning of the analysis. E.g. 12-08-2023. If not specified, the default value is used (One year ago).'),
    'end_date': fields.String(required=False,
                              description='End date represents the beginning of the analysis. E.g. 25-09-2023. If not specified, the default value is used (today)')
})

authentication_parameters = api.model('Parameters for authentication', {
    'mail': fields.String(required=True,
                          description='The email address for the user is missing.'),
    'password': fields.String(required=True,
                              description='The password for the user is missing.')
})

authentication_and_ticker_parameters = api.model('Parameters for authentication and ticker', {

    'ticker': fields.String(required=True,
                            description='The Tickersymbol is missing. Example: {"ticker":"NASDAQ:AAPL"}'),
    'mail': fields.String(required=True,
                          description='The email address for the user is missing.'),
    'password': fields.String(required=True,
                              description='The password for the user is missing.')
})

authentication_and_file_name = api.model('Parameters for authentication and ticker', {

    'file_name': fields.String(required=True, description='Filename'),
    'mail': fields.String(required=True,
                          description='The email address for the user is missing.'),
    'password': fields.String(required=True,
                              description='The password for the user is missing.')
})

"""
Creating the path for saving the plots if it does not exist .
"""
if not os.path.exists('Graphs'):
    os.makedirs('Graphs')


# Endpoint to pull data from the database returns all data
@api.route('/getStocksFromDatabase')
class GetStocksFromDatabase(Resource):
    @api.expect(authentication_parameters)
    def get(self):
        """
        Retrieves all stocks from WebScrapingService.
        :return:
            if authentication successful: Json response from WebScrapingService with all the stocks
            else: Message which tells that the authentication was not successful.
        """
        auth_parser.parse_args()
        if authenticate_user(request.values):
            return get_all_stocks_from_database()
        else:
            return AUTHENTICATION_FAILED


# Endpoint to pull data from the database returns data for a given ticker (specific stock)
@api.route('/getStockFromDatabase')
class GetStockFromDatabase(Resource):
    @api.expect(authentication_and_ticker_parameters)
    def get(self):
        """
        Gets stocks for a given ticker (specific stock)
        :return:
            if authentication was successful:
                if ticker is not Null/None:
                    if get request from Database was successful:
                        Json response from WebScrapingService with the stocks for the given ticker
                    else:
                        {"Successful": False, "Error": Exception}
                else:
                    Str: "Please pass a tickersymbol. Example: {"ticker": "NASDAQ:GOOGL"}."
            else: "Authentication failed. {"mail":"xyz", "password": "1234"}"
        """
        auth_and_ticker_parser.parse_args()
        if authenticate_user(request.values):
            request_values = request.values
            if request.values.get('ticker') is not None:
                try:
                    return stock_from_database(request_values.to_dict())
                except Exception as e:
                    return {"Successful": False, "Error": str(e)}
            else:
                return PASS_A_TICKERSYMBOL
        return AUTHENTICATION_FAILED


# Endpoint to call the analysis function
@api.route('/startAnalysis')
class StartAnalysis(Resource):
    @api.expect(start_analysis_parameters)
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
        start_analysis_parser.parse_args()
        if authenticate_user(request.values):
            request_values = request.values
            if request_values.get('ticker') is not None:
                try:
                    save_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_SAVE_STOCK,
                                 params=request_values.to_dict())
                    stock_response = requests.get(STOCK_WEB_SCRAPING_SERVICE_GET_STOCK_FROM_TICKER,
                                                  params=request_values.to_dict())
                    stocks = stock_response.json()
                    return start_analysis_for_ticker(stocks["Ticker"], stocks["Stocks"], request_values)
                except Exception as e:
                    return {"Successful": False, "Error": str(e)}
            else:
                return PASS_A_TICKERSYMBOL
        return AUTHENTICATION_FAILED


# Endpoint for deleting the png files
@api.route('/deleteFiles')
class DeleteFiles(Resource):
    @api.expect(authentication_and_file_name)
    def get(self):
        """
        Function for deleting the png Files.
        :return:
            if authentication successful:
                if remove successful:
                    {"Successful deleted": "True"}
                else:
                    {"Successful": False, "Error": Exception}
            else: Message which tells that the authentication was not successful.
        """
        auth_and_file_parser.parse_args()
        if authenticate_user(request.values):
            try:
                os.remove(request.values.get('file_name'))
                return {"Successful deleted": "True"}
            except Exception as e:
                return {"Successful": False, "Error": str(e)}
        else:
            return AUTHENTICATION_FAILED


# Endpoint for returning the graph as png
@api.route('/getGraphs')
class GetGraphs(Resource):
    @api.expect(authentication_and_file_name)
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
        auth_and_file_parser.parse_args()
        if authenticate_user(request.values):
            if request.values.get('file_name') is not None:
                file_name = request.values.get('file_name')
                try:
                    if os.path.exists(file_name):
                        return send_file(file_name)
                except Exception as e:
                    return {"Successful": False, "Error": str(e)}
            else:
                return PASS_A_FILENAME
        return AUTHENTICATION_FAILED


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9030"))
