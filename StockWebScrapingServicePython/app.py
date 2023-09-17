import pandas
import requests
from bson.json_util import dumps
from flask import Flask, jsonify, request
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
import datetime as dt
#import get_finance_data
import gspread



#Todo in Flask Config Debug wieder einschalten


app = Flask(__name__)
api = CORS(app)
app.config['JSON_SORT_KEYS'] = False

# Keycloak Konfiguration
REALM_NAME = "stock-information-procurer"
CLIENT_ID = "stockwebscrapingservicepy"
CLIENT_SECRET = "2COhXMhEOb6sw2LSBhvlhgiYwltiKfbI"

# Local Config:
# KEYCLOAK_SERVER = "http://localhost:8080/auth"
# mailserver = "http://localhost:9020"


# Docker Config:
# KEYCLOAK_SERVER = "http://stockinformationprocurer-keycloak-1:8080/auth"
# mailserver = "http://stockinformationprocurer-mail-service-1:9020"
#
#
# def get_version():
#     new_version = 0
#     with open('version.txt', 'r') as reader:
#         txt = reader.read()
#         print(txt)
#         new_version = int(txt) + 1
#     with open('version.txt', 'w') as writer:
#         writer.write(str(new_version))
#     print("Version:", new_version)
#     print("Time", dt.datetime.now())
#
#
# get_version()
#
#
# # Funktion zum Abrufen eines JWT-Tokens von Keycloak
# def get_keycloak_token():
#     token_url = f"{KEYCLOAK_SERVER}/realms/{REALM_NAME}/protocol/openid-connect/token"
#     data = {
#         "grant_type": "client_credentials",
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#     }
#     response = requests.post(token_url, data=data)
#     print(response)
#     if response.status_code == 200:
#         token_data = response.json()
#         access_token = token_data.get("access_token")
#         return access_token
#     else:
#         raise Exception("Fehler beim Abrufen des Keycloak-Tokens")
#
#
# # Middleware für Token-Überprüfung
# @app.before_request
# def check_token():
#     # test_mail()
#     # test_keycloak()
#     if request.endpoint == 'get_test':
#         return  # Keine Authentifizierung erforderlich für /get
#
#     token = request.headers.get('Authorization')
#     print(token)
#     if not token:
#         return jsonify({"message": "Token fehlt"}), 401
#
#     try:
#         # Überprüfen Sie das Token mit Keycloak
#         token = token.replace("Bearer ", "")
#         keycloak_url = f"{KEYCLOAK_SERVER}/realms/{REALM_NAME}/protocol/openid-connect/userinfo"
#         headers = {"Authorization": f"Bearer {token}"}
#         print(headers)
#         response = requests.get(keycloak_url, headers=headers)
#         print(response)
#         print(response.content)
#         print('Json', response.json())
#         if response.status_code == 200:
#             return  # Authentifizierung erfolgreich
#         else:
#             return jsonify({"message": "Ungültiges Token"}), 401
#
#     except Exception as e:
#         return jsonify({"message": str(e)}), 401
#
#
# def test_mail():
#     URL = mailserver + '/get'
#     response = requests.get(URL)
#     print(response)
#     print(response.content)
#
#
# def test_keycloak():
#     URL = "http://stockinformationprocurer-keycloak-1:8080/auth/realms/stock-information-procurer/protocol/openid-connect/userinfo"
#     token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6eHZ2a1JHRjJOdXRsTmJCUEw4U0tjcTcyV3ZkaDVwa3M0cUNLSlpyenNZIn0.eyJleHAiOjE2OTM5OTY2NDksImlhdCI6MTY5Mzk5NjM0OSwianRpIjoiMzM3NzBlNDMtNDU5Zi00Mjk3LTkxY2EtNzExODYyNzM1OTk5IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL2F1dGgvcmVhbG1zL3N0b2NrLWluZm9ybWF0aW9uLXByb2N1cmVyIiwiYXVkIjpbImFjY291bnQiLCJkb2N1bWVudC1zZXJ2aWNlIl0sInN1YiI6ImYwYjgzNDVhLWJjZTMtNDdiZS1hYjM5LTIwYjYyYWY1ODEzNCIsInR5cCI6IkJlYXJlciIsImF6cCI6InN0b2Nrd2Vic2NyYXBpbmdzZXJ2aWNlcHkiLCJzZXNzaW9uX3N0YXRlIjoiMWFiNzI2OWItZTMxYy00MjQ2LTg1YjgtYTc4MWMxMzhlOTQxIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLXN0b2NrLWluZm9ybWF0aW9uLXByb2N1cmVyIiwib2ZmbGluZV9hY2Nlc3MiLCJhZG1pbiIsInVtYV9hdXRob3JpemF0aW9uIiwidXNlciJdfSwicmVzb3VyY2VfYWNjZXNzIjp7InN0b2Nrd2Vic2NyYXBpbmdzZXJ2aWNlcHkiOnsicm9sZXMiOlsiY2xpZW50X3VzZXIiLCJjbGllbnRfYWRtaW4iXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfSwiZG9jdW1lbnQtc2VydmljZSI6eyJyb2xlcyI6WyJjbGllbnRfdXNlciIsImNsaWVudF9hZG1pbiJdfX0sInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsInNpZCI6IjFhYjcyNjliLWUzMWMtNDI0Ni04NWI4LWE3ODFjMTM4ZTk0MSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoidGltbSJ9.Wq1p782ZQRcPoqrujKDozNHrUEu0hr-4Au_QfFA8o1v5H7NeZR_8DlUkYdcyXTWN4zXTnqRdNv7S-FY18CufYVA-QnGtEd-KI_yRD55s___eJZj8Ikmax1QKrAKZepiVUHwU1zSuYED0DpZi0hUXcnjt67YnnKvHI0AqmntsjMMwaGy5waIV6azJncFfoMmtMvMpHxzD50cUv1j2gAuUVmTKiETx0S3DmYjHBt4t7whShq3ezED3zeHnPdJAMa9f_jck4VMlv_lBaeRczCoKCP78RJP1Jqy823CI4TmuGTBXzPlv79bsR9nXzF4HxCsZ841ObJeNqvafsLHq-66FeQ"
#     headers = {"Authorization": f"Bearer {token}"}
#     response = requests.get(URL, headers=headers)
#     print(response)
#     print(response.content)
#
#
# @app.route('/get', methods=['GET'])
# def get_test():
#     return 'Successful'
#
#
# @app.route('/testmongo_upload', methods=['GET'])
# def test_mongo_upload():
#     # Verbindung zur MongoDB-Datenbank herstellen
#     client = MongoClient("mongodb://mongodb:27017/")
#     db = client["stockinformations"]
#
#     collection = db["stocks"]
#
#     # Beispiel-Daten zum Einfügen
#     data_to_insert = [
#         {"symbol": "AAPL", "price": 150.25, "volume": 200},
#         {"symbol": "GOOGL", "price": 2800.50, "volume": 800},
#         {"symbol": "AMZN", "price": 3500.75, "volume": 950}
#     ]
#
#     # Daten in die Datenbank einfügen
#     for entry in data_to_insert:
#         print(entry)
#         collection.insert_one(entry)
#
#     return "Daten erfolgreich eingefügt."
#
#
# @app.route('/testmongo_get', methods=['GET'])
# def test_mongo_get():
#     print('Get Test:')
#     # Verbindung zur MongoDB-Datenbank herstellen
#     # client = MongoClient("mongodb://mongodb/")
#     client = MongoClient("mongodb://mongodb:27017/")
#     db = client["stockinformations"]
#
#     collection = db["stocks"]
#     entries = collection.find()
#     entries_as_json = dumps(entries)
#     return entries_as_json
#
#
# @app.route('/testdocument', methods=['GET'])
# def test_document():
#     # BASE_URL = 'http://stockinformationprocurer-document-service-1:9010'
#     URL = mailserver + '/get'
#     response = requests.get(URL)
#     print(response)
#     print(response.content)
#     return response.content

# GET-ENDPUNKT für einen spezifischen Tracker
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    # Übergabeparameter = Ticker
    input_text = request.args.get('text', '')

    ticker = input_text

    filepath = "stockinformationprocurer-f97f16464594.json"
    #filepath = ".\stockinformationprocurer-f97f16464594.json"
    filename = "Stock_Data"
    worksheet_name = "Stock_Data_WS"
    #ticker = 'NASDAQ:TSLA'
    cell = 'A1'

    # connect_to_gsheet(filepath, filename)
    gc = gspread.service_account(filename=filepath)
    sh = gc.open(filename)

    worksheet_name = worksheet_name
    try:
        worksheet = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=worksheet_name, rows=1000, cols=1000)

    worksheet.update(cell, ticker)

    # get stock data as df
    stock_data = pandas.DataFrame(worksheet.get_all_values())

    # set values at [1] as column title
    stock_data.columns = stock_data.iloc[1]

    # drop values at [0] and [1]
    stock_data = stock_data.iloc[2:]

    # set date (daily) as index
    stock_data.set_index('Date', inplace=True)

    stock_data = stock_data.to_json()

    return stock_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
