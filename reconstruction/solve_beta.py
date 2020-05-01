import os
import sys
import argparse
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt 
from beta_solver import BetaSolver
from common_utils import get_population, get_country_data, strip_year,lockdown_info 
import matplotlib.dates as mdates
import datetime

conv = np.vectorize(mdates.strpdate2num('%Y-%m-%d'))

def split_average_diff (data):
   # split the data into two parts - before day 'i' and after 
   # day 'i' and compute the difference between these two parts
   # 'i' is varied from day 1 to day (n-1).
   # Note that data for the first few and last few days
   # will not be used to draw any conclusion.

   y = np.zeros ([data.shape[0]])
   for i in range (1, data.shape[0]-2):
     a1 = np.mean (data[:i])
     a2 = np.mean (data[i:])
     y[i]  = a1 - a2
   return y 


def plot_data (args, beta, lockdown_date):

   days = [int(i) for i in range(0, beta.shape[0])]

   lockdown = beta.index.get_loc(lockdown_date, method ='ffill')

   print("lockdown day:",lockdown)

   fig = plt.figure(figsize=(12,8))
   ax = fig.add_subplot(111)
   ax.set_title(args.country_name)
   ax.set_ylabel(r'$\beta (t)$')
   ax.set_xlabel('t')

   fig.autofmt_xdate()
   ax.axhline(y=0,c='k',ls='--')
   ax.axvline(x=lockdown+1,c='k',ls='--')


   ax.plot(days[1:-2], beta[1:-2])
   ax.plot(days[1:-2], beta[1:-2],'o')
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   ax.grid()

   plt.show()


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')
   parser.add_argument('-c','--country-name',help='Country name',\
      default='Italy')
   parser.add_argument('-o','--output-dir',help='Output dir',\
      default='results')
   parser.add_argument('-g','--gamma-in',help='Parameter 1/gama',type=float,default=7)
   parser.add_argument('-s','--sigma-in',help='Parameter 1/sigma',type=float,default=7)
   parser.add_argument('-a','--alpha',help='Alpha',type=float,default=1)


   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)
   df = pd.read_csv(args.input_file)

   df = df[df['confirmed'] > 25] 

   N, L, T = lockdown_info(args.lockdown_file,  args.country_name)
   df = get_country_data (df, args.country_name)

   R = BetaSolver (df, N)
   beta = R.solve(args.gamma_in, args.sigma_in, args.alpha)
   
   plot_data (args, beta, L)
   

