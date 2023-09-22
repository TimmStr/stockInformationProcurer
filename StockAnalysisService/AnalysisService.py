import json
from datetime import datetime, timedelta

from matplotlib import pyplot as plt
from Path.paths import GRAPHS
import numpy as np
import time

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
    return GRAPHS + ticker + volume + '_' + date + ".png"


def prepare_data(stocks):
    date = list(stocks["Open"].keys())
    open_val = stocks["Open"]
    high_val = stocks["High"]
    low_val = stocks['Low']
    close_val = stocks['Close']
    volume = stocks['Volume']
    dates, open_vals, high_vals, low_vals, close_vals, volume_vals = [], [], [], [], [], []
    for day in date:
        dates.append(day.replace('.', '-')[:10])
        open_vals.append(float(open_val.get(day).replace(',', '.')))
        high_vals.append(float(high_val.get(day).replace(',', '.')))
        low_vals.append(float(low_val.get(day).replace(',', '.')))
        close_vals.append(float(close_val.get(day).replace(',', '.')))
        volume_vals.append(int(volume.get(day)))
    return dates, open_vals, high_vals, low_vals, close_vals, volume_vals


def data_for_time_period(start_date, end_date, dates, open_vals, high_vals, low_vals, close_vals, volume_vals):
    start_date = time.strptime(start_date, "%d-%m-%Y")
    end_date = time.strptime(end_date, "%d-%m-%Y")
    dates_for_time_period, open_vals_for_time_period, high_vals_for_time_period, \
    low_vals_for_time_period, close_vals_for_time_period, volume_vals_for_time_period = [], [], [], [], [], []
    for index, date in enumerate(dates):
        if start_date <= time.strptime(date, "%Y-%m-%d") <= end_date:
            dates_for_time_period.append(date)
            open_vals_for_time_period.append(open_vals[index])
            high_vals_for_time_period.append(high_vals[index])
            low_vals_for_time_period.append(low_vals[index])
            close_vals_for_time_period.append(close_vals[index])
            volume_vals_for_time_period.append(volume_vals[index])
    return dates_for_time_period, \
           open_vals_for_time_period, \
           high_vals_for_time_period, \
           low_vals_for_time_period, \
           close_vals_for_time_period, \
           volume_vals_for_time_period


def start_analysis_for_ticker(ticker, stocks, request_values):
    stocks = json.loads(stocks)
    print(request_values.keys())

    if 'start_date' in request_values.keys() and 'end_date' in request_values.keys():
        start_date = request_values['start_date']
        end_date = request_values['end_date']
    else:
        end_date = datetime.today()
        end_date = end_date.strftime('%d-%m-%Y')
        start_date = datetime.today() - timedelta(days=365)
        start_date = start_date.strftime('%d-%m-%Y')
    dates, open_vals, high_vals, low_vals, close_vals, volume_vals = prepare_data(stocks)
    dates_for_time_period, open_vals_for_time_period, high_vals_for_time_period, low_vals_for_time_period, close_vals_for_time_period, volume_vals_for_time_period = data_for_time_period(
        start_date,
        end_date,
        dates,
        open_vals,
        high_vals,
        low_vals,
        close_vals,
        volume_vals)

    file_names = draw_graph(ticker, dates_for_time_period, close_vals_for_time_period, low_vals_for_time_period,
                            high_vals_for_time_period, volume_vals_for_time_period)
    print('Avg', str((sum(open_vals_for_time_period) / len(open_vals_for_time_period))), 'Max',
          str(max(high_vals_for_time_period)), 'Min', str(min(low_vals_for_time_period)), 'Filename', file_names)
    return {'Avg': format((sum(open_vals_for_time_period) / len(open_vals_for_time_period)),'.2f'),
            'Max': format(max(high_vals_for_time_period),'.2f'),
            'Min': format(min(low_vals_for_time_period),'.2f'), 'Filename': file_names}


def get_x_axis(dates):
    dates_length = len(dates)
    if dates_length < 8:
        return dates
    else:
        new_date_indices = []
        x = int(dates_length / 8)
        print(x)

        for i, date in enumerate(dates):
            print(str(i), str(x), str(i / x), str(i % x))
            if i % x == 0 or i == 0:
                new_date_indices.append(date[2:])
        return new_date_indices


def draw_graph(ticker, dates, close_vals, low_vals, high_vals, volume_vals):
    filenames = []
    new_date_indices = get_x_axis(dates)
    plt.title(ticker + '  Daily price: ' + 'Start:' + str(dates[0]) + ' - End:' + str(dates[-1]))
    plt.plot(dates, close_vals, color='b', label='Close')
    plt.plot(dates, high_vals, color='g', label='High')
    plt.plot(dates, low_vals, color='r', label='Low')
    plt.xlabel("Day")
    plt.ylabel("Price $")
    # plt.grid(True)
    plt.legend()
    plt.xticks(np.arange(0, len(dates), int(len(dates) / 8)), new_date_indices, rotation=30)
    filename = get_filename(ticker, str(dates[-1]))
    plt.savefig(filename)
    filenames.append(filename)
    plt.clf()

    plt.plot(dates, volume_vals, color='b', label='Volume')
    plt.title(ticker + '  Daily volume: ' + 'Start:' + str(dates[0]) + ' - End:' + str(dates[-1]))
    plt.xlabel("Day")
    plt.ylabel("Volume")
    # plt.grid(True)
    plt.legend()
    plt.xticks(np.arange(0, len(dates), int(len(dates) / 8)), new_date_indices, rotation=30)
    filename = get_filename(ticker, str(dates[-1]), '_volume')
    plt.savefig(filename)
    filenames.append(filename)
    plt.clf()

    return filenames
