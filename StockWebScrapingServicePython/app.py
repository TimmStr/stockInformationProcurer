import requests
from bson.json_util import dumps
from flask import Flask, jsonify, request
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
print('version 7')


# Keycloak Konfiguration
REALM_NAME = "stock-information-procurer"
CLIENT_ID = "stockwebscrapingservicepy"
CLIENT_SECRET = "2COhXMhEOb6sw2LSBhvlhgiYwltiKfbI"


#Local Config:
KEYCLOAK_SERVER = "http://localhost:8080/auth"
mailserver = "http://localhost:9020"


#Docker Config:
# KEYCLOAK_SERVER = "http://stockinformationprocurer-keycloak-1:8080/auth"
# mailserver = "stockinformationprocurer-mail-service-1:9020"




# Funktion zum Abrufen eines JWT-Tokens von Keycloak
def get_keycloak_token():
    token_url = f"{KEYCLOAK_SERVER}/realms/{REALM_NAME}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    print(response)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        return access_token
    else:
        raise Exception("Fehler beim Abrufen des Keycloak-Tokens")


# Middleware für Token-Überprüfung
@app.before_request
def check_token():
    if request.endpoint == 'get_test':
        return  # Keine Authentifizierung erforderlich für /get

    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return jsonify({"message": "Token fehlt"}), 401

    try:
        # Überprüfen Sie das Token mit Keycloak
        token = token.replace("Bearer ", "")
        keycloak_url = f"{KEYCLOAK_SERVER}/realms/{REALM_NAME}/protocol/openid-connect/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        print(headers)
        response = requests.get(keycloak_url, headers=headers)
        print(response)
        if response.status_code == 200:
            return  # Authentifizierung erfolgreich
        else:
            return jsonify({"message": "Ungültiges Token"}), 401

    except Exception as e:
        return jsonify({"message": str(e)}), 401


@app.route('/get', methods=['GET'])
def get_test():
    return 'Successful'


@app.route('/testmongo_upload', methods=['GET'])
def test_mongo_upload():
    # Verbindung zur MongoDB-Datenbank herstellen
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["stockinformations"]

    collection = db["stocks"]

    # Beispiel-Daten zum Einfügen
    data_to_insert = [
        {"symbol": "AAPL", "price": 150.25, "volume": 200},
        {"symbol": "GOOGL", "price": 2800.50, "volume": 800},
        {"symbol": "AMZN", "price": 3500.75, "volume": 950}
    ]

    # Daten in die Datenbank einfügen
    for entry in data_to_insert:
        print(entry)
        collection.insert_one(entry)

    return "Daten erfolgreich eingefügt."


@app.route('/testmongo_get', methods=['GET'])
def test_mongo_get():
    print('Get Test:')
    # Verbindung zur MongoDB-Datenbank herstellen
    # client = MongoClient("mongodb://mongodb/")
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["stockinformations"]

    collection = db["stocks"]
    entries = collection.find()
    entries_as_json = dumps(entries)
    return entries_as_json


@app.route('/testdocument', methods=['GET'])
def test_document():
    # BASE_URL = 'http://stockinformationprocurer-document-service-1:9010'
    URL = mailserver + '/get'
    response = requests.get(URL)
    print(response)
    print(response.content)
    return response.content


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
