import sys
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd 
import matplotlib.pyplot as plt 


def func(x, a, b, c):
   return a * np.exp(-b * x) 

if __name__ == "__main__":
    
    df = pd.read_csv(sys.argv[1])

    df_in = df[df['Country/Region'] == 'India']

    dates = df_in['ObservationDate'].to_list()
    dates = [x.replace('/2020','') for x in dates]

    deaths = df_in['Deaths'].to_list()    

    print("dates:",dates)
    print("deaths:",deaths)

    for i in range(0, len(dates)):
       print(i, dates[i], deaths[i])

    dates_1 = dates[40:55]
    deaths_1 = deaths[40:55]

    y_full = deaths[40:]
    dates_full = dates[40:] 

    x_full = np.array([i for i in range(0, len(y_full))])
    
    xdata = np.array([ i for i in range(0, len(dates_1))])
    ydata = np.array([float(x) for x in  deaths_1]) 

    plt.plot(x_full, y_full, 'bo',label='Full data' )
    plt.plot(xdata, ydata, 'ro',label='Fitted data')
    
    popt, pcov = curve_fit(func, xdata, ydata)

    print("params:",popt[0],popt[1],popt[1])

    plt.plot(x_full, func(x_full, *popt), 'r-',\
      label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.xticks(x_full, dates_full, rotation=90) 
    plt.legend()
    

    plt.show()
