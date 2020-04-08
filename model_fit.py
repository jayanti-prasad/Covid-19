import os
import sys
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd 
import matplotlib.pyplot as plt 
import argparse
import datetime

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")


def func(x, a, b):

   return a * np.exp(-b * x)   

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input cvv file')
   parser.add_argument('-s', '--start-day', help='Star day for fitting data',type=int,default=10)
   parser.add_argument('-e', '--end-day', help='End day for fitting data', type=int,default=20)
   parser.add_argument('-o', '--output-dir', help='Output dir',default="plots")
   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   df = pd.read_csv(args.input_file)

   for index, rows in df.iterrows():
      print(index, rows['date'], rows['confirmed'],rows['recovered'],rows['deaths'])


   start = args.start_day
   end = args.end_day 

   dates = df['date'].to_list() 
   dates = [str(d).replace("-2020","") for d in dates] 

   days = np.array([float(i) for i in range(0, len(dates))])

   cases=["deaths","recovered","confirmed"]

   yy = [] 
   for case in cases:
      tt = df[case].to_list()
      yy.append(tt) 
 

   fig = plt.figure(figsize=(18,18))

   ax = [] 
   ax.append(plt.subplot(311))
   ax.append(plt.subplot(312))
   ax.append(plt.subplot(313))

   for i in range(0, len(cases)):
      ax[i].plot(dates, yy[i], 'bo',label='Full data' )
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
      ax[i].set_ylabel(cases[i])
      ax[i].grid()
      if i < 2 :
         ax[i].set_xticklabels([])
      if i == 0: 
         ax[i].set_title("Covid-19 data fitting [a*exp(-b*x)] for India, created@: " + now)
         
      start = 0 
      for j in range(0, len(yy[i])):
         if start == 0 and yy[i][j] > 0:
            start = j

      x_fit = np.array(days[start:end]-days[start])
      dates_fit = np.array(dates[start:end])
      y_fit = np.array(yy[i][start:end])
 
      ax[i].plot(dates_fit, y_fit, 'ro',label='Fitting data' )
      popt, pcov = curve_fit(func, x_fit, y_fit)
      print("coeff:",popt) 

      ax[i].plot(dates[start:], func(days[start:]-days[start], *popt), 'k-',\
         label='fit: a=%5.3f, b=%5.3f' % tuple(popt))
      ax[i].legend()
  
   plt.savefig(args.output_dir + os.sep + "exp_model_fit.pdf")

