"""
This file includes many functions to get the data from the google sheets.
"""
import gspread
import pandas as pd
from flask import jsonify


def get_worksheet_from_gspread(ticker):
    """
    The ticker modifies the Google sheet using gspread. This pulls the complete history of stock prices for the ticker from the Google API.
    :param ticker: str
    :return:
        Google Worksheet
    """
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


def get_worksheet_from_kpis(ticker):
    """
    The ticker modifies the Google sheet using gspread. This pulls the latest information of the definied KPIs from the Google API for a specific ticker.
    :param ticker: str
    :return:
        Google Worksheet
    """
    filepath = "stockinformationprocurer-f97f16464594.json"
    filename = "Stock_Data"
    worksheet_name = "KPIs"
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
    """
    Creates a worksheet with the ticker. It transforms the worksheet into a dataframe and returns the dataframe as json.
    :param ticker:
    :return:
        json
    """
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
    """
    Creating a list of dictionaries. Each dictionary represents a row in the worksheet.
    :param ticker: str
    :return:
        list of dict
    """
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


def get_kpis_as_dict(ticker):
    """
    Creating a dictionary with the keys and values of the KPIs.
    :param ticker:
    :return:
    """
    worksheet = get_worksheet_from_kpis(ticker)
    kpis = worksheet.get_all_values()
    ticker = kpis[0][0]
    kpi_as_dict = {
        "Ticker": ticker,
    }
    for item in kpis[1:]:
        key = item[0]
        value = item[1]
        kpi_as_dict[key] = value
    return kpi_as_dict
