import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from common_utils import date_normalize, strip_year, get_country_data 
import matplotlib
from reconstruction import Reconstruct

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
   parser.add_argument('-s','--start-date',help='Start date',type=int, default=0)
   parser.add_argument('-o','--output-dir',help='Output dir',default="results")
   parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')

   args = parser.parse_args()

   df = pd.read_csv(args.input_file)
   df = get_country_data (df, args.country_name)

   df = df[df['confirmed'] > 25]
   
   X = df['confirmed'].to_numpy()  
   Y = df['deaths'].to_numpy()  
   Z = df['recovered'].to_numpy()  
   dates = strip_year (df['date'].to_list())
   R = Y + Z  
   I = X - R

  
   It = np.array([ X[i+1] - X[i] for i in range(0, X.shape[0]-1)])
   It =  It / np.sum (It)
  
  
   beta = np.zeros (X.shape[0]-1)

   for i in range(0, I.shape[0]-1):
     beta[i] = ((I[i+1]-I[i]) + (R[i+1]-R[i]))/ I[i]

   t = dates[:-1]

   R = Reconstruct(args, args.country_name)
   g, s, a = 7.0, 7.0, 1.0
   R.solve (g, s, a)
   beta1 = R.beta[:-2]  


   beta = beta / np.sum(beta)
   beta1 = beta1 / np.sum(beta1)


   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot()  
   It = I / np.sum (I)

   ax.plot(t, It[:-1],c='k')
   ax.scatter(t, It[:-1],c='k')
   ax.plot(t, beta,'o',c='b')
   ax.plot(t, beta,label='Direct',c='b')
   ax.plot(t[:-1], beta1,label='Reconstructed',c='r')
   ax.plot(t[:-1], beta1,'o',c='r')
   ax.set_xlabel('t')
   ax.set_ylabel(r'$\beta (t)$')
   ax.set_title(args.country_name)
   plt.legend()
   ax.axhline(y=0,c='k',ls='--')
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right',fontsize=10)
   plt.savefig(args.output_dir + os.sep + "beta_" + args.country_name + ".pdf")
   plt.show() 

   
