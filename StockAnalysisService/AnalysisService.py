from matplotlib import pyplot as plt
from Path.paths import GRAPHS


def start_analysis_for_ticker(ticker, stocks):
    date, open_val, high_val, low_val, close_val, volume = [], [], [], [], [], []

    print('Start Anyalysis')
    print(stocks)
    for entry in stocks:
        print(entry)
        sys.exit()
        date.append(entry.get('Date'))
        open_val.append(float(entry.get('Open')))
        high_val.append(float(entry.get('High')))
        low_val.append(float(entry.get('Low')))
        close_val.append(float(entry.get('Close')))
        volume.append(int(entry.get('Volume')))
    print(open_val)
    filename = draw_graph(ticker, date, close_val, high_val, volume)
    return {'Avg:': (sum(open_val) / len(open_val)), 'Max:': max(high_val), 'Min': min(low_val), 'Filename': filename}


def draw_graph(ticker, date, close_val, high_val, volume):
    plt.plot(date, close_val, color='b', label='Close')
    plt.plot(date, high_val, color='g', label='High')
    plt.xlabel("Day")
    plt.ylabel("Price $")
    plt.grid(True)
    plt.legend()
    filename = GRAPHS + ticker + str(date[-1]) + ".png"
    plt.savefig(filename)

    plt.plot(date, volume, color='b', label='Close')
    plt.xlabel("Day")
    plt.ylabel("Volume")
    plt.grid(True)
    plt.legend()
    filename = GRAPHS + ticker + "-volume" + str(date[-1]) + ".png"
    plt.savefig(filename)

    return filename
