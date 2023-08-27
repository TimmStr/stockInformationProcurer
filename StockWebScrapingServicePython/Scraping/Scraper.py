from datetime import datetime

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


def string_to_digit(stock_value):
    return_value = ''
    for digit in stock_value:
        if not digit.isdigit():
            if digit == ',':
                return_value += '.'
            elif digit == '-':
                return_value += '-'
        else:
            return_value = return_value + digit
    return return_value


def get_data_for_symbol(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    url = f'https://de.finance.yahoo.com/quote/{symbol}'

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    name = symbol
    date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    price = string_to_digit(soup.find('div', {'class': 'D(ib) Mend(20px)'}).find('fin-streamer').text)
    price_change = string_to_digit(str(soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[0].text))
    price_change_percent = string_to_digit(
        str(soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text))
    return {'Name': name,
            'Date': date,
            'Price': price,
            'Price Change': price_change,
            'Price Change %': price_change_percent}


def get_historical_data(symbol):
    data = yf.download(symbol, '2016-01-01', '2019-08-01')
    return data


liste = ['AMZN', 'AAPL', 'MSFT', 'BABA', 'TCEHY', 'BTC-USD', 'ETH-USD']
# for symbol in liste:
#     print(get_data_for_symbol(symbol))

# print(get_historical_data('AAPL'))
ticker = yf.Ticker('AAPL')
ticker.get_financials()
pnl = ticker.financials
bs = ticker.balancesheet
cf = ticker.cashflow
info = ticker.info
print(ticker.fast_info)
# print(ticker.info)
fs = pd.concat([pnl, bs, cf])
# print(fs.to_string())
# for row in fs:
#     print(row)
# print(fs)
# print(yf.Ticker('AAPL').get_financials())
# print(yf.Ticker('AAPL').balancesheet)
