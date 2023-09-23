"""
Defines multiple functions for multiple different purposes:
    - Preprocessing the Data
    - Retrieving Data for a timeperiod
    - Calling an analysis on specific stock data
    - Drawing graphs for the stock data

This can be seen as the main functions of the application. It returns relevant stock data for a given ticker
like "NASDAQ:AMZN and analyzes the data as well as drawing the data in plot. A ticker specifies a stock, when it's
passed with an identifier for a specific stock exchange  like "NASDAQ" the StockWebScrapingService will return the
stock data in respect to the given stock exchange as prices and historic data can vary between stock exchanges.
"""
import json
from datetime import datetime, timedelta

from matplotlib import pyplot as plt
from Utils.paths import GRAPHS
import numpy as np
import time


def get_filename(ticker, date='', volume=''):
    """
    Generates a filename for given ticker, date and volume.
    :param ticker: str
    :param date: str
    :param volume: str
    :return: str
        Example:
            Graph for stockprice: "GRAPHS/NASDAQ_NVDA_18_09_2023"
            Graph for volume: "GRAPHS/NASDAQ_NVDA_volume_18_09_2023"
    """
    ticker = ticker.replace(':', '_')
    date = date.replace('.', '_')
    date = date.replace(':', '-')
    return GRAPHS + ticker + volume + '_' + date + ".png"


def data_preprocessing(stocks):
    """
    Lists the different date values and save the individual dictionary values in their own lists.
    The "," are replaced by "." replaced.
    In addition, the different date values are converted into a uniform format.
    :param stocks: Dictionary with the date as key
    :return:
        List of str: Dates,
        List of float: Open Values (Value at the beginning of a day),
        List of float: High Values (highest Value for a day),
        List of float: Low Values (lowest Value for a day),
        List of float: CLose Values (Value at the end of a day),
        List of int: Volume Values (How many stocks have beend traded)
    """
    date = list(stocks["Open"].keys())
    open_val, high_val, low_val, close_val, volume = stocks["Open"], stocks["High"], stocks['Low'], stocks['Close'], \
                                                     stocks['Volume']
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
    """
    Reads all the values from List dates. If the value is between start_date and end_date, the values that are standing
    in the same index will be stored in the specific "xyz_for_time_period" List.
    :param start_date: str
    :param end_date: str
    :param dates: List of str
    :param open_vals: List of float
    :param high_vals: List of float
    :param low_vals: List of float
    :param close_vals: List of float
    :param volume_vals: List of int
    :return:
        List of str: Dates for time period,
        List of float: Open values for time period,
        List of float: High values for time period,
        List of float: Low values for time period,
        List of float: Close values for time period,
        List of int: Volumes for time period
    """
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
    return dates_for_time_period, open_vals_for_time_period, high_vals_for_time_period, \
           low_vals_for_time_period, close_vals_for_time_period, volume_vals_for_time_period


def start_analysis_for_ticker(ticker, stocks, request_values):
    """
    Important function.Is responsible for calling the individual functions.
    It first loads the transferred stocks into a dictionary and reads the start and end dates of the query.
    The data_preprocessing function is then called. There the data is converted into the correct formats.
    The result is passed into the “data_for_time_period” function with the start and end date.
    The result from the previous function is then used to call the “draw_graph” function, which draws the graphs using
    the data transferred and returns the file names under which the graphs were saved.
    :param ticker: str,
    :param stocks: dict,
    :param request_values: dict,
    :return: dict{
        'Avg' :float,
        'Max': float,
        'Min': float,
        'Filename: List of str}
    """
    stocks = json.loads(stocks)
    if 'start_date' in request_values.keys() and 'end_date' in request_values.keys():
        start_date = request_values['start_date']
        end_date = request_values['end_date']
    else:
        end_date = datetime.today()
        end_date = end_date.strftime('%d-%m-%Y')
        start_date = datetime.today() - timedelta(days=365)
        start_date = start_date.strftime('%d-%m-%Y')
    dates, open_vals, high_vals, low_vals, close_vals, volume_vals = data_preprocessing(stocks)
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
    return {'Avg': format((sum(open_vals_for_time_period) / len(open_vals_for_time_period)), '.2f'),
            'Max': format(max(high_vals_for_time_period), '.2f'),
            'Min': format(min(low_vals_for_time_period), '.2f'), 'Filename': file_names}


def get_x_axis(dates, interval=8):
    """
    Is responsible for making the x-axis of the plot clearer. This function limits the number of values displayed
    on the x-axis to the size of the interval (default = 8). If the length of the list is smaller than than the
    interval, it gets immediately returned.
    :param dates: List str
    :param interval: int
    :return: List str
        Example:
            dates = [01-09-2023, 02-09-2023, 03-09-2023, 04-09-2023, 05-09-2023, 06-09-2023, 07-09-2023, 08-09-2023]
            interval = 3

        return new_date_indeces = [01-09-2023, 04-09-2023, 06-09-2023]
    """
    dates_length = len(dates)
    if dates_length < interval:
        return dates
    else:
        new_date_indices = []
        x = int(dates_length / interval)
        for i, date in enumerate(dates):
            if i % x == 0 or i == 0:
                new_date_indices.append(date[2:])
        return new_date_indices


def draw_graph(ticker, dates, close_vals, low_vals, high_vals, volume_vals):
    """
    Draws two graphs (One for the prices and another for the volumes) for the given data.
    :param ticker: str
    :param dates: list of str
    :param close_vals: list of float
    :param low_vals: list of float
    :param high_vals: list of float
    :param volume_vals: list of int
    :return: List of str
        Example:
            filenames = ["NASDAQ_NVDA__18_09_2023 16-00-00.png", "NASDAQ_NVDA_volume_18_09_2023 16-00-00.png"]
    """
    interval = 8
    filenames = []

    # Graph for the price
    new_date_indices = get_x_axis(dates, interval)
    plt.title(ticker + '  Daily price: ' + 'Start:' + str(dates[0]) + ' - End:' + str(dates[-1]))
    plt.plot(dates, close_vals, color='b', label='Close')
    plt.plot(dates, high_vals, color='g', label='High')
    plt.plot(dates, low_vals, color='r', label='Low')
    plt.xlabel("Day")
    plt.ylabel("Price $")
    plt.legend()
    plt.xticks(np.arange(0, len(dates), int(len(dates) / interval)), new_date_indices, rotation=30)
    filename = get_filename(ticker, str(dates[-1]))
    plt.savefig(filename)
    filenames.append(filename)
    plt.clf()

    # Graph for the volume
    plt.plot(dates, volume_vals, color='b', label='Volume')
    plt.title(ticker + '  Daily volume: ' + 'Start:' + str(dates[0]) + ' - End:' + str(dates[-1]))
    plt.xlabel("Day")
    plt.ylabel("Volume")
    plt.legend()
    plt.xticks(np.arange(0, len(dates), int(len(dates) / 8)), new_date_indices, rotation=30)
    filename = get_filename(ticker, str(dates[-1]), '_volume')
    plt.savefig(filename)
    filenames.append(filename)
    plt.clf()

    return filenames
