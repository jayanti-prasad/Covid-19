import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common_utils import strip_year, get_country_data 
from common_utils import lockdown_info
from beta_solver import BetaSolver 

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country name')
   parser.add_argument('-o','--output-dir',help='Output dir',default="results")
   parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')

   args = parser.parse_args()

   df = pd.read_csv(args.input_file)
   df = get_country_data (df, args.country_name)

   df = df[df['confirmed'] > 25]
   df.index = df['date'].to_list()  
 
   C = df['confirmed'] 
   D = df['deaths']  
   R = df['recovered']
  
   R = R + D  
   I = C - R

   dI = I.diff(periods=1).iloc[1:]
   dR = R.diff(periods=1).iloc[1:]
   I1 = I.iloc[1:]

   # equation (11) of arXiv:2003.00122v5
   beta1 = (dI + dR).divide(I1, fill_value=0)

   # For our reconstruction 
   N, L, T = lockdown_info (args.lockdown_file, args.country_name)
   R = BetaSolver(df, N)
   beta2 = R.solve(7.0, 7.0, 1.0).iloc[1:-2]


   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot()  

   beta1.index = strip_year(beta1.index)
   beta2.index = strip_year(beta2.index)

   ax.plot(beta1,'o',c='b')
   ax.plot(beta1,label='Direct',c='b')
   ax.plot(beta2,label='Reconstructed',c='r')
   ax.plot(beta2,'o',c='r')
   ax.set_xlabel('t')
   ax.set_ylabel(r'$\beta (t)$')
   ax.set_title(args.country_name)
   plt.legend()
   ax.axhline(y=0,c='k',ls='--')
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right',fontsize=10)
   plt.show() 

   
