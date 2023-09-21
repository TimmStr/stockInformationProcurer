import json

from matplotlib import pyplot as plt
from Path.paths import GRAPHS

"""
Defines functions for 3 different porposes:
    - Stock data by ticker and date
    - Calling an analysis on specific stock data
    - drawing graphs for the stock data

 This can be seen as the main functions of the application. It returns relevant stock data for a given ticker like "NASDAQ:AMZN and analyzes
 the data as well as drawing the data in plot. A ticker specifies a stock, when it's passed with an identifier for a specific stock exchange
 like "NASDAQ" the Google Finance API will return the stock data in respect to the given stock exchange as prices and historic data can
 vary between stock exchanges.
"""

# generates a filename for given ticker, date and volume
def get_filename(ticker, date='', volume=''):
    ticker = ticker.replace(':', '_')
    date = date.replace('.', '_')
    date = date.replace(':', '-')
    return GRAPHS + ticker + '_' + volume + '_' + date + ".png"


# analyzes the data for a stock in respect to a given ticker
def start_analysis_for_ticker(ticker, stocks):
    stocks = json.loads(stocks)
    print(stocks.keys())
    date = list(stocks["Open"].keys())
    open_val = list(stocks["Open"].values())
    high_val = list(stocks["High"].values())
    low_val = list(stocks['Low'].values())
    close_val = list(stocks['Close'].values())
    volume = list(stocks['Volume'].values())

    open_val = [float(val.replace(',', '.')) for val in open_val]
    high_val = [float(val.replace(',', '.')) for val in high_val]
    low_val = [float(val.replace(',', '.')) for val in low_val]
    close_val = [float(val.replace(',', '.')) for val in close_val]
    volume = [int(val) for val in volume]
    print('Date', len(date), date[:5])
    print('Open', len(open_val), open_val[:5])
    print('High', len(high_val), high_val[:5])
    print('Low', len(low_val), low_val[:5])
    print('Close', len(close_val), close_val[:5])
    print('Volume', len(volume), volume[:5])

    filename = draw_graph(ticker, date, close_val, high_val, volume)
    return {'Avg:': (sum(open_val) / len(open_val)), 'Max:': max(high_val), 'Min': min(low_val), 'Filename': filename}

# draws a plot out of the data for a specific stock in respect to a given ticker
def draw_graph(ticker, date, close_val, high_val, volume):
    filenames = []
    plt.plot(date, close_val, color='b', label='Close')
    plt.plot(date, high_val, color='g', label='High')
    plt.xlabel("Day")
    plt.ylabel("Price $")
    plt.grid(True)
    plt.legend()
    filename = get_filename(ticker, str(date[-1]))
    plt.savefig(filename)
    filenames.append(filename)

    plt.plot(date, volume, color='b', label='Close')
    plt.xlabel("Day")
    plt.ylabel("Volume")
    plt.grid(True)
    plt.legend()
    filename = get_filename(ticker, str(date[-1]), 'volume')
    plt.savefig(filename)
    filenames.append(filename)

    return filenames


