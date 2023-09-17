# Quelle1: https://codesolid.com/google-sheets-in-python-and-pandas/
# Quelle2: https://docs.gspread.org/en/latest/oauth2.html

import gspread
import pandas as pd
import numpy as np
from gspread_dataframe import get_as_dataframe, set_with_dataframe
#from gsheet_to_dataframe import sh, worksheet
#from gspread import worksheet

filepath = ".\stockinformationprocurer-f97f16464594.json"
filename = "Stock_Data"
worksheet_name = "Stock_Data_WS"
ticker = 'NASDAQ:TSLA'
cell = 'A1'

#connect_to_gsheet(filepath, filename)
gc = gspread.service_account(filename=filepath)
sh = gc.open(filename)

def connect_to_gsheet(filepath, filename):
    gc = gspread.service_account(filename=filepath)
    sh = gc.open(filename)

def read_worksheet(worksheet_name):
    # Read worksheet or create if doesn't exist
    worksheet_name = worksheet_name
    try:
        worksheet = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(title=worksheet_name, rows=1000, cols=1000)

def update_ticker(ticker, cell):
    # update google sheet cell with a ticker
    ticker = ticker
    worksheet.update(cell, ticker)


def get_finance_data(filepath, filename, worksheet_name, ticker, cell):
    # create connection to google sheets via credentials file
    # connect_to_gsheet(filepath, filename)
    # read specific worksheet
    read_worksheet(worksheet_name)
    # update ticker
    update_ticker(ticker, cell)

    # get stock data as df
    stock_data = pd.DataFrame(worksheet.get_all_values())

    # set values at [1] as column title
    stock_data.columns = stock_data.iloc[1]

    # drop values at [0] and [1]
    stock_data = stock_data.iloc[2:]

    # set date (daily) as index
    stock_data.set_index('Date', inplace=True)

    return stock_data.to_json()

stock_data = get_finance_data(filepath, filename, worksheet_name, ticker, cell)


print(stock_data)

