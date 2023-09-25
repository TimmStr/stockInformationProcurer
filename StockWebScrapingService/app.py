from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint

from MongoDb.MongoService import *
from Scraper.gspread_scraper import *
from Utils.messages import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True

"""
Swagger config. The json file is available at "http://localhost:9040/swagger.json" while the official Swagger UI URL
is available under "http://localhost:9040/api/docs/".
"""
SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:9040/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Stock Web Scraping Service"
    }
)

app.register_blueprint(swaggerui_blueprint)

"""
Defines the parameter that are required for some functions.
Example: The data for a stock cannot be pulled, if there is no symbol given. 
"""
ticker_parameter = api.model('Parameter', {
    'ticker': fields.String(required=True, description='Das Tickersymbol z.B. NASDAQ:AAPL')
})


@api.route('/getStockFromTicker')
class GetStockFromTicker(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        """
        Function that returns stockprices for a Stockticker.
        Expects ticker_parameter = str E.g.: "ticker":"NASDAQ:AAPL"
        :return:
            dict {"Ticker":"...", "Stocks": "..."} if stockinformation can be pulled from google sheet
            dict {"Successful":"False", "Error":"..."} if stockinformation can not be pulled from google sheet
            str if Tickersymbol is None
        """
        request_values = request.values
        ticker = request_values.get('ticker')
        if ticker is not None:
            try:
                return {"Ticker": ticker, "Stocks": get_stock_data_as_json(ticker)}
            except Exception as e:
                return {"Successful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/getKpisFromTicker')
class GetKpisFromTicker(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        """
        Function that returns Key performance indicators for a Stockticker.
        Expects ticker_parameter = str E.g.: "ticker":"NASDAQ:AAPL"
        :return:
            dict {"KPIs":"..."} if kpis can be pulled from google sheet
            dict {"Successful":"False", "Error":"..."} if stockinformation can not be pulled from google sheet
            str if Tickersymbol is None
        """
        request_values = request.values
        if request_values.get('ticker') is not None:
            try:
                return {"KPIs": get_kpis_as_dict(request.values.get('ticker'))}
            except Exception as e:
                return {"Successful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/saveStock')
class SaveStock(Resource):
    @api.expect(ticker_parameter)
    def put(self):
        """
        Function that stores stockinformation in the mongo database.
        Expects ticker_parameter = str E.g.: "Ticker":"NASDAQ:AAPL"
        :return:
            dict if call of the "save_stock_in_database" function was successful
            dict {"Successful":"False", "Error":"..."} if function call was not successful
            str if Tickersymbol is None
        """
        if request.values.get('ticker') is not None:
            try:
                return save_stock_in_database(request.values.get('ticker'))
            except Exception as e:
                return {"Successful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/getAllStocks')
class GetAllStocks(Resource):
    def get(self):
        """
        Function that stores stockinformation in the mongo database.
        :return:
            dict if call of the "get_all_stocks_from_mongo_db" function was successful
            dict {"Successful":"False", "Error":"..."} if function call was not successful
        """
        try:
            return get_all_stocks_from_mongo_db()
        except Exception as e:
            return {"Successful": False, "Error": str(e)}


@api.route('/getStocksFromDatabaseWithTicker')
class GetStocksFromDatabaseWithTicker(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        """
        Function that returns stockinformations from mongo database.
        Expects ticker_parameter = str E.g.: "ticker":"NASDAQ:AAPL"
        :return:
            dict if call of the "get_stock_from_mongo_db" function was successful
            dict {"Successful":"False", "Error":"..."} if function call was not successful
            str if Tickersymbol is None
        """
        if request.values.get('ticker') is not None:
            try:
                return get_stock_from_mongo_db(request.values.get('ticker'))
            except Exception as e:
                return {"Successful": False, "Error": str(e)}
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/deleteAllStocks')
class DeleteAllStocks(Resource):
    def get(self):
        """
        Function that deletes all entries from mongo database.
        It is only included for demonstration/testing.
        :return:
            str if delete_all_stocks_from_mongo_db() function call was successful.
            dict {"Successful":"False", "Error":"..."} if function call was not successful

        """
        try:
            delete_all_stocks_from_mongo_db()
            return STOCKS_DELETED
        except Exception as e:
            return {"Successful": False, "Error": str(e)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
