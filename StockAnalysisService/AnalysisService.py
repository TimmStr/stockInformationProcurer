import json
from datetime import datetime

from matplotlib import pyplot as plt
from Path.paths import GRAPHS


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


# def data_for_time_period(start_date, end_date, dates, open_vals, high_vals, low_vals, close_vals, volume_vals):
#     start_date = datetime.date(start_date)
#     end_date = datetime.date(end_date)
#     dates_for_time_period, open_vals_for_time_period, high_vals_for_time_period, \
#     low_vals_for_time_period, close_vals_for_time_period, volume_vals_for_time_period = [], [], [], [], [], []
#     for index, date in enumerate(dates):
#         if start_date <= datetime.date(date) <= end_date:
#             dates_for_time_period.append(date)
#             open_vals_for_time_period.append(open_vals[index])
#             high_vals_for_time_period.append(high_vals[index])
#             low_vals_for_time_period.append(low_vals[index])
#             close_vals_for_time_period.append(close_vals[index])
#             volume_vals_for_time_period.append(volume_vals[index])
#     return dates_for_time_period, \
#            low_vals_for_time_period, \
#            close_vals_for_time_period, \
#            volume_vals_for_time_period, \
#            close_vals_for_time_period, \
#            volume_vals_for_time_period


def start_analysis_for_ticker(ticker, stocks):
    stocks = json.loads(stocks)
    dates, open_vals, high_vals, low_vals, close_vals, volume_vals = prepare_data(stocks)
    # dates_for_time_period, open_vals_for_time_period, high_vals_for_time_period, low_vals_for_time_period, close_vals_for_time_period, volume_vals_for_time_period = data_for_time_period(
    #     '22-09-2022',
    #     '22-09-2023',
    #     dates,
    #     open_vals,
    #     high_vals,
    #     low_vals,
    #     close_vals,
    #     volume_vals)

    # file_names = draw_graph(ticker, dates_for_time_period, close_vals_for_time_period, low_vals_for_time_period, high_vals_for_time_period, volume_vals_for_time_period)
    # return {'Avg': (sum(dates_for_time_period) / len(dates_for_time_period)), 'Max': max(high_vals_for_time_period), 'Min': min(low_vals_for_time_period), 'Filename': filename}
    file_names = draw_graph(ticker, dates, close_vals, low_vals,
                            high_vals, volume_vals)

    print(file_names)
    for date, open_val, high_val, low_val, close_val, volume_val in zip(dates, open_vals, high_vals, low_vals,
                                                                        close_vals, volume_vals):
        print(date, open_val, high_val, low_val, close_val, volume_val)

    print('Avg', str(sum(open_vals) / len(open_vals)), 'Max', str(max(high_vals)), 'Min', str(min(low_vals)), 'Filename',
          file_names)

    return {'Avg': str(sum(open_vals) / len(open_vals)), 'Max': str(max(high_vals)),
            'Min': str(min(low_vals)), 'Filename': file_names}


def draw_graph(ticker, date, close_vals, low_vals, high_vals, volume_vals):
    filenames = []
    plt.plot(date, close_vals, color='b', label='Close')
    plt.plot(date, high_vals, color='g', label='High')
    plt.plot(date, low_vals, color='r', label='Low')
    plt.xlabel("Day")
    plt.ylabel("Price $")
    # plt.grid(True)
    plt.legend()
    filename = get_filename(ticker, str(date[-1]))
    plt.savefig(filename)
    filenames.append(filename)
    plt.clf()

    plt.plot(date, volume_vals, color='b', label='Volume')
    plt.xlabel("Day")
    plt.ylabel("Volume")
    # plt.grid(True)
    plt.legend()
    filename = get_filename(ticker, str(date[-1]), '_volume')
    plt.savefig(filename)
    filenames.append(filename)
    plt.clf()

    return filenames
