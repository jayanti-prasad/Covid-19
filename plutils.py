import os
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib 
from date_utils import strip_year 
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

line_width=2

font = {'family' : 'normal',
        'size'   : 12}
matplotlib.rc('font', **font)
matplotlib.rcParams['axes.linewidth'] = line_width 


def plot_data (df, columns, flag, title, skip_days, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(3, 1, sharex=True)
    fig.set_figheight(18)
    fig.set_figwidth(18)
    plt.subplots_adjust(hspace=.0)

    date_form = DateFormatter("%m-%d")
    colors = ['red','green','blue']

    for i in range (0, len(columns)):
    
        Y = df[columns[i]]
        dY = Y.diff(periods=1).iloc[1:]
   
        plt.setp(ax[i].get_xticklabels(), rotation=45, horizontalalignment='right')
        ax[2].xaxis.set_major_formatter(date_form)
        # Ensure a major tick for each week using (interval=1) 
        ax[2].xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

        ax[i].yaxis.tick_right()
        ax[i].ticklabel_format(style='plain', axis='y')
 

        if flag > 0:
            ax[i].plot(dY,c=colors[i],linewidth=line_width)
            ax[i].plot(dY,'.',c=colors[i])
        else:
            ax[i].plot(Y,c=colors[i],linewidth=line_width)
            ax[i].plot(Y,'.',c=colors[i])
  
        ax[i].set_ylabel(columns[i])
        ax[i].grid()
        if i == 0:
           ax[i].set_title("Covid-19 [" + title +"]")

    plt.savefig(output_dir + os.sep + title.replace(" ","") +".pdf")
    print("output:",output_dir + os.sep + title.replace(" ","") +".pdf")
    #fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
  
