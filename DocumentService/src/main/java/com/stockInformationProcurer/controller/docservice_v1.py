from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data for documents
documents = [
    {"id": 1, "title": "Document 1", "content": "This is the content of Document 1"},
    {"id": 2, "title": "Document 2", "content": "This is the content of Document 2"},
]

@app.route('/documents', methods=['GET'])
def get_documents():
    return jsonify(documents)

@app.route('/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    document = next((doc for doc in documents if doc['id'] == doc_id), None)
    if document:
        return jsonify(document)
    else:
        return jsonify({"error": "Document not found"}), 404

@app.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json()
    if 'title' in data and 'content' in data:
        new_document = {
            "id": len(documents) + 1,
            "title": data['title'],
            "content": data['content']
        }
        documents.append(new_document)
        return jsonify(new_document), 201
    else:
        return jsonify({"error": "Missing 'title' or 'content' in request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
