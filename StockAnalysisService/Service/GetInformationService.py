from Path.paths import *
import requests

"""
Defines two methods to get stock information in two ways with different arguments:
    - All stock data available in MongoDB-Database
    - Specific stock data which is been described by an ticker argument
"""


# return every stock data as JSON-FIle
def get_all_stocks_from_database():
    URL = STOCK_WEB_SCRAPING_SERVICE + 'get_all_stocks'
    response = requests.get(URL)
    return response.json()

# ticker describes specific stock data, return data as JSON-File
def stock_from_database(ticker):
    URL = STOCK_WEB_SCRAPING_SERVICE + 'get_stocks_from_database_with_ticker'
    response = requests.get(URL, params=ticker)
    return response.json()
