# coding=<UTF-8>

import matplotlib.pyplot as plt
from datetime import datetime
import os


class Plotter:
    dates = []
    temps = []
    usage = []
    max_val = 100

    def __init__(self, log_file=".temp.log"):
        plt.style.use('seaborn-whitegrid')

        with open(log_file, 'r') as f:
            for line in f.readlines():
                spl = line.split(";")

                date = datetime.strptime(spl[0], '%d/%m/%Y %H:%M:%S')

                self.dates.append(date)
                self.temps.append(float(spl[1]))
                self.usage.append(float(spl[2]))

                self.max_val = max(max(self.temps), max(self.usage))

    def do_plot(self):
        self.fig, self.ax1 = plt.subplots()

        color = 'tab:red'
        self.ax1.set_xlabel('Datetime')

        self.ax1.set_ylabel('Temp in C', color=color)
        self.ax1.plot(self.dates, self.temps, color=color)
        self.ax1.tick_params(axis='y', labelcolor=color)

        self.ax2 = self.ax1.twinx()  # instantiate a second axes that shares the same x-axis

        a,b = 0, (int(int(self.max_val+5.5)/10)*10+1)
        self.ax1.set_ylim(a,b)
        self.ax2.set_ylim(a,b)

        color = 'tab:blue'

        self.ax2.set_ylabel('% usage', color=color)  # we already handled the x-label with ax1
        self.ax2.plot(self.dates, self.usage, color=color)
        self.ax2.tick_params(axis='y', labelcolor=color)

        # beautify the x-labels
        plt.gcf().autofmt_xdate()

        self.fig.tight_layout()  # otherwise the right y-label is slightly clipped

    def show(self):
        plt.show()

    def save(self, location="./", name="plot", format_="svg"):
        plt.savefig(os.path.join(location, name), format=format_)
