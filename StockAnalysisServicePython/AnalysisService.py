import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime


def start_analysis_for_symbol(collection, symbol='TSLA'):
    entries = collection.find({"Symbol": symbol})
    print(entries)
    date, open_val, high_val, low_val, close_val, volume = [], [], [], [], [], []
    for entry in entries:
        date.append(entry.get('Date'))
        open_val.append(float(entry.get('Open')))
        high_val.append(float(entry.get('High')))
        low_val.append(float(entry.get('Low')))
        close_val.append(float(entry.get('Close')))
        volume.append(int(entry.get('Volume')))
    print(open_val)
    draw_graph(symbol, date, close_val, high_val, volume)
    return {'Avg:': (sum(open_val) / len(open_val)), 'Max:': max(high_val), 'Min': min(low_val)}


def draw_graph(symbol, date, close_val, high_val, volume):
    plt.plot(date, close_val, color='b', label='Close')
    plt.plot(date, high_val, color='g', label='High')
    plt.xlabel("Day")
    plt.ylabel("Price $")
    plt.grid(True)
    plt.legend()
    plt.savefig(symbol+str(date[-1])+".png")
    return date[0]
