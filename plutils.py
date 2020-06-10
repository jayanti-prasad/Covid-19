import os
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib 
from date_utils import strip_year 

line_width=3

font = {'family' : 'normal',
        'size'   : 18}
matplotlib.rc('font', **font)
matplotlib.rcParams['axes.linewidth'] = line_width 


def plot_data (df, columns, flag, title, skip_days, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    dates = strip_year (df['date'].to_list())
    days  = [int(i) for i in range(0, len(dates))]

    fig, ax = plt.subplots(3, 1, sharex=True)
    fig.set_figheight(18)
    fig.set_figwidth(18)
    plt.subplots_adjust(hspace=.0)

    colors = ['red','green','blue']

    for i in range (0, len(columns)):
    
        Y = df[columns[i]]
        dY = Y.diff(periods=1).iloc[1:]

        labels = [dates[i] for i in range(0, len(days))  if i% skip_days == 0]
        plt.xticks(np.arange(0,len(days), skip_days), labels)

        plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')

        if flag > 0:
            ax[i].plot(dates[1:], dY,c=colors[i],linewidth=line_width)
            ax[i].plot(dates[1:], dY,'o',c=colors[i])
        else:
            ax[i].plot(dates, Y,c=colors[i],linewidth=line_width)
            ax[i].plot(dates, Y,'o',c=colors[i])
  
        ax[i].set_ylabel(columns[i])
        ax[i].grid()
        if i == 0:
           ax[i].set_title(title)

    plt.savefig(output_dir + os.sep + title.replace(" ","") +".pdf")
    print("output:",output_dir + os.sep + title.replace(" ","") +".pdf")
    plt.show()
  
