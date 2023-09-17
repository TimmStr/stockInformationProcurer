import gspread
import pandas as pd


def get_worksheet_from_gspread(ticker):
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
    return worksheet


def get_stock_data_as_json(ticker):
    worksheet = get_worksheet_from_gspread(ticker)
    # get stock data as df
    stock_data = pd.DataFrame(worksheet.get_all_values())

    # set values at [1] as column title
    stock_data.columns = stock_data.iloc[1]

    # drop values at [0] and [1]
    stock_data = stock_data.iloc[2:]

    # set date (daily) as index
    stock_data.set_index('Date', inplace=True)

    return stock_data.to_json()


def get_stock_data_as_list_of_dicts(ticker):
    worksheet = get_worksheet_from_gspread(ticker)
    columns = worksheet.get_all_values()[1]
    values = worksheet.get_all_values()[2:]
    values_as_dict = []
    for entry in values:
        values_as_dict.append(
            {
                "Ticker": ticker,
                columns[0]: entry[0],
                columns[1]: entry[1],
                columns[2]: entry[2],
                columns[3]: entry[3],
                columns[4]: entry[4],
                columns[5]: entry[5],
            }
        )
    return values_as_dict
