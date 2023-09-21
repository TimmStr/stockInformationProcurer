import json

from matplotlib import pyplot as plt
from Path.paths import GRAPHS


def get_filename(ticker, date='', volume=''):
    ticker = ticker.replace(':', '_')
    date = date.replace('.', '_')
    date = date.replace(':', '-')
    return GRAPHS + ticker + '_' + volume + '_' + date + ".png"


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


