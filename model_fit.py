import os
import sys
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd 
import argparse
from common_utils import date_normalize

def func(x, a, b):
   return a * np.exp(-b * x)   

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input csv file')
   parser.add_argument('-c', '--country', help='Country',default='India')
   parser.add_argument('-s', '--start-day', help='Star day for fitting data',type=int,default=10)
   parser.add_argument('-e', '--end-day', help='End day for fitting data', type=int,default=80)
   parser.add_argument('-o', '--output-dir', help='Output dir',default="plots")
   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   df = pd.read_csv(args.input_file)
   df = df[df['country'] == args.country]

   df = date_normalize (df)
   df = df.sort_values(by='dates')
   
   dates = [d.replace('2020-','') for d in df['dates'].to_list()]

   x = np.array([float(i) for i in range(0, len(dates))])

   start = args.start_day
   end = args.end_day 

   cases=["deaths","recovered","confirmed"]

   fig = plt.figure(figsize=(18,18))

   ax = [plt.subplot(311)]
   ax.append(plt.subplot(312))
   ax.append(plt.subplot(313))

   #for i in range(0, 1):
   for i in range(0, len(cases)):
      y = df[cases[i]].to_list()

      ax[i].plot(dates, y, 'bo',label='Full data' )
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
      ax[i].set_ylabel(cases[i])
      ax[i].grid()

      if i < 2 :
         ax[i].set_xticklabels([])
      if i == 0: 
         ax[i].set_title("Covid-19 data fitting [a*exp(-b*x)] for:" + args.country)
         
      start = 0 
      for j in range(0, len(y)):
        if start == 0 and y[j] > 0:
           start = j

      x_fit = np.array(x[start:end]-x[start])
      dates_fit = dates[start:end]
      y_fit = np.array(y[start:end])

      print("x_fit:",x_fit)
      print("y_fit:",y_fit)
  
      ax[i].plot(dates_fit, y_fit, 'ro',label='Fitting data' )
      popt, pcov = curve_fit(func, x_fit, y_fit)
      print("coeff:",popt) 

      y_predict = func(x_fit, *popt) 

      print("y_predict:",y_predict) 
      ax[i].plot(dates_fit, y_predict, 'k-',\
         label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
      ax[i].legend()
  
   plt.savefig(args.output_dir + os.sep + args.country + "_model_fit.pdf")

