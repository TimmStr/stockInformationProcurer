from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint

from MongoDb.MongoService import *
from Scraper.gspread_scraper import *
from Utils.messages import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True

# URL for Swagger UI
SWAGGER_URL = '/api/docs'
# Location of the swagger.json
API_URL = 'http://localhost:9040/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Stock Web Scraping Service"
    }
)

app.register_blueprint(swaggerui_blueprint)


ticker_parameter = api.model('Parameter', {
    'ticker': fields.String(required=True, description='Das Tickersymbol z.B. NASDAQ:AAPL')
})

@api.route('/get_stock_from_ticker')
class GetStockFromTicker(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        ticker = request.values.get('ticker')
        if ticker:
            try:
                return {"Ticker": ticker, "Stocks": get_stock_data_as_json(ticker)}
            except:
                return ERROR_OCCURED
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/get_kpis_from_ticker')
class GetKpisFromTicker(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        if request.values.get('ticker') is not None:
            try:
                return {"KPIs": get_kpis_as_dict(request.values.get('ticker'))}
            except:
                return ERROR_OCCURED
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/save_stock')
class SaveStock(Resource):
    @api.expect(ticker_parameter)
    def put(self):
        if request.values.get('ticker') is not None:
            try:
                data_dicts = get_stock_data_as_list_of_dicts(request.values.get('ticker'))
                return save_data_dicts(data_dicts)
            except:
                return ERROR_OCCURED
        else:
            return PASS_A_TICKERSYMBOL


@api.route('/get_all_stocks')
class GetAllStocks(Resource):
    def get(self):
        try:
            return get_all_stocks_from_mongo_db()
        except:
            return ERROR_OCCURED


@api.route('/delete_all_stocks')
class DeleteAllStocks(Resource):
    def get(self):
        try:
            delete_all_stocks_from_mongo_db()
            return STOCKS_DELETED
        except:
            return ERROR_OCCURED


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
