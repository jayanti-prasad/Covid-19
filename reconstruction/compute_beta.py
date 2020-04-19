import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from common_utils import date_normalize, strip_year 
import matplotlib

fontsize = 22
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)
matplotlib.rcParams['axes.linewidth'] = 2.0
matplotlib.rcParams["font.family"] = "Courier New"



if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country name')
   parser.add_argument('-s','--start-date',help='Start data',type=int, default=0)
   parser.add_argument('-o','--output-dir',help='Output dir',default="results")

   args = parser.parse_args()

   df = pd.read_csv(args.input_file)

   df = df.replace({'United Kingdom': 'UK'}, regex=True)

   df = df[df['country'] == args.country_name]
   df = date_normalize (df)
   df = df.sort_values(by='date')

   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]
   
   X = df['confirmed'].to_numpy()  
   Y = df['deaths'].to_numpy()  
   Z = df['recovered'].to_numpy()  
   dates = strip_year (df['date'].to_list())
   X = X - Y - Z 
  
   beta = np.zeros (X.shape[0]-1)

   for i in range(0, X.shape[0]-1):
     beta[i] = ((X[i+1]-X[i]) + (Z[i+1]-Z[i]))/ X[i]


   t = dates[args.start_date:-2]
   x = beta[args.start_date:-1]

   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot()  

   ax.plot(t, x,'o')
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right',fontsize=10)
   ax.axhline(y=0,c='k',ls='--')
   ax.plot(t, x)
   ax.set_xlabel('t')
   ax.set_ylabel(r'$\beta (t)$')
   ax.set_title(args.country_name)
   plt.savefig(args.output_dir + os.sep + "beta_" + args.country_name + ".pdf")
 





   
