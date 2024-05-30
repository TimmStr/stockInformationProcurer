import pandas as pd
import yfinance as yf
from Utils.paths import STOCKS, CSV_EXTENSION
import os

tickers_list = ['AAPL', 'MSFT', 'IBM', 'NVDA']

for ticker in tickers_list:
    data = yf.download(ticker, '2019-1-1')
    data.to_csv(os.path.join(STOCKS, f'{ticker}{CSV_EXTENSION}'))
