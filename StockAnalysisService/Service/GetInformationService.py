from Path.paths import *
import requests


def get_all_stocks_from_database():
    URL = STOCK_WEB_SCRAPING_SERVICE + 'get_all_stocks'
    response = requests.get(URL)
    return response.json()


def stock_from_database(ticker):
    URL = STOCK_WEB_SCRAPING_SERVICE + 'get_stocks_from_database_with_ticker'
    response = requests.get(URL, params=ticker)
    return response.json()
