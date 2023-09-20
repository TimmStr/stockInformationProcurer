import gspread
import pandas
from flask import Flask, request
from flask_restful import Api

# Define FLASK App
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

# 'Hello World! Endpoint - for testing purpose'
@app.route('/')
def hello_world():
    return 'Hello, World!'

# GET-Endpoint used to get stock data
@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    # ticker defines stocks to get data for
    ticker = request.values.get('symbol')

    # JSON file for Auth purposes in Google Sheets API
    filepath = "stockinformationprocurer-f97f16464594.json"

    # defines name of Google Sheet
    filename = "Stock_Data"

    # defines specific worksheet in a Google Sheet
    worksheet_name = "Stock_Data_WS"

    # Defines a cell to manipulate -> used to update specific ticker
    cell = 'A1'

    # opens a connection to Google Sheet via Google Sheets API
    gc = gspread.service_account(filename=filepath)
    sh = gc.open(filename)

    # try to read worksheet, if not existent create
    worksheet_name = worksheet_name
    try:
        worksheet = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=worksheet_name, rows=1000, cols=1000)

    # update specific cell with a ticker
    worksheet.update(cell, ticker)

    # get stock data as df
    stock_data = pandas.DataFrame(worksheet.get_all_values())

    # set values at [1] as column title
    stock_data.columns = stock_data.iloc[1]

    # drop values at [0] and [1]
    stock_data = stock_data.iloc[2:]

    # set date (daily) as index
    stock_data.set_index('Date', inplace=True)

    # convert data to JSON
    stock_data = stock_data.to_json()

    # defines return value
    return stock_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int("9040"))
