import os
import sys
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd 
import matplotlib.pyplot as plt 
import argparse


def func(x, a, b, c):
   return a * np.exp(-b * x)  

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input cvv file')
   parser.add_argument('-s', '--start-day', help='Star day for fitting data',type=int)
   parser.add_argument('-e', '--end-day', help='End day for fitting data', type=int)
   parser.add_argument('-o', '--output-dir', help='Output dir')
   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   df = pd.read_csv(args.input_file)
   start = args.start_day
   end = args.end_day 

   df_in = df[df['Country/Region'] == 'India']

   dates = df_in['ObservationDate'].to_list()
   dates = [x.replace('/2020','') for x in dates]

   deaths = df_in['Deaths'].to_list()    
   confirmed = df_in['Confirmed'].to_list()    

   fit_deaths = deaths[start:end]
   fit_confirmed = confirmed[start:end]
   fit_dates = dates[start:end]

   full_dates = dates[start:] 
   full_deaths= deaths[start:]
   full_confirmed = confirmed[start:]

   full_days  = np.array([i for i in range(0, len(full_deaths))])

   xdata = np.array([ i for i in range(0, len(fit_dates))])

   fig = plt.figure(figsize=(12,6))

   ax1 = plt.subplot(121)
   ax2 = plt.subplot(122)

   ydata = np.array([float(x) for x in  fit_deaths]) 

   ax1.plot(full_dates, full_deaths, 'bo',label='Full data' )
   ax1.plot(fit_dates, fit_deaths, 'ro',label='Fitted data')
    
   popt, pcov = curve_fit(func, xdata, ydata)

   print("params:",popt[0],popt[1],popt[1])

   ax1.plot(full_days, func(full_days, *popt), 'k-',\
     label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
   #ax1.set_xticks(full_days, full_dates, rotation=90) 
   plt.setp(ax1.get_xticklabels(), rotation=90, horizontalalignment='right')
   ax1.set_title("Number of deaths")
   ax1.grid()
   ax1.legend()
    

   ydata = np.array([float(x) for x in  fit_confirmed])

   ax2.plot(full_dates, full_confirmed, 'bo',label='Full data' )
   ax2.plot(fit_dates, fit_confirmed, 'ro',label='Fitted data')

   popt, pcov = curve_fit(func, xdata, ydata)

   print("params:",popt[0],popt[1],popt[1])

   ax2.plot(full_days, func(full_days, *popt), 'k-',\
     label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
   #ax1.set_xticks(full_days, full_dates, rotation=90) 
   plt.setp(ax2.get_xticklabels(), rotation=90, horizontalalignment='right')
   ax2.set_title("Number of Confimed cases")
   ax2.grid()
   ax2.legend()
   plt.savefig(args.output_dir + os.sep + "india_data_fitted.pdf")

