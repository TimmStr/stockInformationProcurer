import gspread
import pandas
from flask import Flask, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    ticker = request.values.get('symbol')

    filepath = "stockinformationprocurer-f97f16464594.json"
    filename = "Stock_Data"
    worksheet_name = "Stock_Data_WS"
    cell = 'A1'

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
