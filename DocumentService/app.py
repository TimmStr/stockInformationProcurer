from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

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

# Dummy data for documents
documents = [
    {"id": 1, "title": "Document 1", "content": "This is the content of Document 1"},
    {"id": 2, "title": "Document 2", "content": "This is the content of Document 2"},
]


@api.route('/documents')
class GetDocuments(Resource):
    def get(self):
        return jsonify(documents)

    def post(self):
        data = request.get_json()
        dict_keys = list(request.get_json().keys())
        if 'title' in dict_keys and 'content' in dict_keys:
            new_document = {
                "id": len(documents) + 1,
                "title": data['title'],
                "content": data['content']
            }
            documents.append(new_document)
            return new_document, 201
        else:
            return jsonify({"error": "Missing 'title' or 'content' in request"}), 400


@api.route('/documents/<int:doc_id>')
class GetDocument(Resource):
    def get(self, doc_id):
        document = next((doc for doc in documents if doc['id'] == doc_id), None)
        if document:
            return jsonify(document)
        else:
            return jsonify({"error": "Document not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9010"))
