import os
import sys
import argparse 
import numpy as np
import pandas as pd

from PyCov19.tcoeff import get_tcoeff 
from data_utils import get_country_data, get_fitting_data
from date_utils import strip_year
from cov_utils import  get_population,get_top_countries
from plot_utils import show_fitting
from plot_frame import plot_frame 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PyCov')
    parser.add_argument('-i', '--input-file', help='Input file')
    parser.add_argument('-o', '--output-dir', help='Output dir')
   
    args = parser.parse_args()

    dF = pd.read_csv(args.input_file)

    countries = list (set (dF['country'].to_list()))

    dfb = pd.DataFrame(columns=['country','beta_min','beta_max','beta_mean','beta_med',\
       'gamma_min','gamma_max','gamma_mean','gamma_med','delta_min','delta_max','delta_mean','delta_med'])

    count = 0  
    for country in countries:
       df = get_country_data (dF, country)
       df = df[df['confirmed']-df['recovered']-df['deaths'] > 25 ]
       if df.shape[0] < 50:
          continue 

       dfc = get_tcoeff (df)
       dfc = dfc.replace(np.nan, 0)
       #dfc = dfc.dropna()
       #print(dfc['date'].to_list())

       dfc.index = strip_year (dfc['date'].to_list())

       beta = dfc['beta']
       gamma = dfc['gamma']
       delta = dfc['delta']

       beta  = beta [beta > 0]
       gamma  = gamma [gamma > 0]
       delta  = delta [delta > 0]

       data = [country, np.min(beta), np.max (beta), np.mean (beta),np.median(beta),\
          np.min(gamma), np.max (gamma), np.mean (gamma),np.median(gamma),\
          np.min(delta), np.max (delta), np.mean (delta),np.median(delta)]

       data[1:] = [ "%.3f" %  d for d in data[1:]]
   

       print(count, data)  

       dfb.loc[count] =  data 
       count +=1
       if dfc.shape[0] > 30:
           plot_frame(dfc, country,args.output_dir) 

    dfb = dfb.dropna()

    dfb.to_csv("bounds.csv") 

