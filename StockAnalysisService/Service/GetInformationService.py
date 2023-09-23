from Utils.paths import *
import requests

"""
Defines two methods to get stock information in two ways with different arguments:
    - All stock data available in MongoDB-Database
    - Specific stock data which is been described by an ticker argument
"""


def get_all_stocks_from_database():
    """
    Retrieves all the stock data from StockWebScrapingService
    :return:
        Json response from StockWebScrapingService
    """
    URL = STOCK_WEB_SCRAPING_SERVICE + 'get_all_stocks'
    response = requests.get(URL)
    return response.json()


def stock_from_database(ticker):
    """
    Retrieves stock data for a ticker from StockWebScrapingService
    :param ticker:
    :return:
        Json response from StockWebScrapingService
    """
    URL = STOCK_WEB_SCRAPING_SERVICE + 'get_stocks_from_database_with_ticker'
    response = requests.get(URL, params=ticker)
    return response.json()
