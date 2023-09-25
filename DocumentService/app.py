"""
Service for creating PDF documents for freely selectable stock tickers and time periods.
"""
from flask import Flask, request, send_file
from flask_restx import Api, Resource, fields, reqparse
from flask_swagger_ui import get_swaggerui_blueprint

from pdf_service import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True

"""
Swagger config. The json file is available at "http://localhost:9010/swagger.json" while the official Swagger UI URL
is available under "http://localhost:9010/api/docs/".
"""
SWAGGER_URL = '/api/docs'
API_URL = 'http://localhost:9010/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Document Service"
    }
)

app.register_blueprint(swaggerui_blueprint)

"""
Defines the parameter that are required for the get function.
Example: The data for a stock cannot be pulled, if there is no symbol given. 
"""
parser = reqparse.RequestParser()
parser.add_argument('ticker', type=str, required=True,
                    help='The Tickersymbol is missing. Example: {"ticker":"NASDAQ:AAPL"}')
parser.add_argument('mail', type=str, required=True, help='The email address for the user is missing.')
parser.add_argument('password', type=str, required=True, help='The password for the user is missing.')
parser.add_argument('start_date', type=str, required=False,
                    help='Start date represents the beginning of the analysis. E.g. 12-08-2023. If not specified, the default value is used (One year ago).')
parser.add_argument('end_date', type=str, required=False,
                    help='End date represents the beginning of the analysis. E.g. 25-09-2023. If not specified, the default value is used (today)')

"""
Defines the parameter for the Swagger UI.
"""
pdf_parameters = api.model('PdfParameters', {
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


@api.route('/createPdf')
class CreatePdf(Resource):
    @api.expect(pdf_parameters)
    def get(self):
        """
        The function first sends a request with the parameters to the Stock Analysis Service.
        This creates an analysis for the ticker. The product of this includes, among other things, max and min values
        for the entire period and the creation of the graphs. The graphs are then saved on the local server.
        The PDF document is then created and issued to the user.
        :return:
            Bytecode for PDF-document
        """
        parser.parse_args()
        request_values = request.values
        filenames, avg_value, max_value, min_value, kpis = stock_information_for_ticker_from_analysis_service(request_values.to_dict())
        pdf_name = create_pdf(filenames, avg_value, max_value, min_value, kpis)
        return send_file(pdf_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9010"))
