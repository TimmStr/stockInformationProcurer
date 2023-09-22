import json

from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
from pdf_service import *

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = True

# URL for Swagger UI
SWAGGER_URL = '/api/docs'
# Location of the swagger.json
API_URL = 'http://localhost:9010/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Document Service"
    }
)

app.register_blueprint(swaggerui_blueprint)
ticker_parameter = api.model('Parameter', {
    'ticker': fields.String(required=True, description='Das Tickersymbol z.B. NASDAQ:AAPL')
})


#
@api.route('/documents')
class GetDocuments(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        ticker = request.values.get('ticker').replace(':', '_')
        filename = create_pdf(ticker)
        return send_file(filename)


@api.route('/createPdf')
class GetDocumentFilenames(Resource):
    @api.expect(ticker_parameter)
    def get(self):
        request_values = request.values
        ticker = request.values.get('ticker')
        filenames, avg_value, max_value, min_value = get_files(request_values.to_dict())
        pdf_name = create_pdf(filenames, avg_value, max_value, min_value)
        print(pdf_name)
        return send_file(pdf_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9010"))
