import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import argparse 
import datetime
from common_utils import date_normalize, get_country_data,strip_year 
from common_utils import get_country_data_owid,get_country_data_kaggle

from datetime import date
import matplotlib 

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

matplotlib.rc('font', **font)



"""
Plot daily time series data for a country. 

"""

def get_country_data_owid (df, country):
   df = df.fillna(0)
   df = df [df['location'] == country]
   df = df[['date','total_cases','total_deaths','total_tests']].copy()
   df.rename(columns = {'date':'date', 'total_cases':'confirmed','total_deaths':'deaths','total_tests':'tests'},\
      inplace = True)

   df = df.sort_values(by='date')
   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]
   df.index = df['date'].to_list()

   return df



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='/Users/jayanti/Data/COVID-19/India/owid-covid-data.csv')

    parser.add_argument('-o','--output-dir',help='Output dir',default='output')
    parser.add_argument('-c','--country-name',help='Country name',default='India')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.input_file)

    df = get_country_data_owid (df, args.country_name)

    #df = df.dropna()
    df = df [df['tests'] > 0]

    dates = strip_year (df['date'].to_list())

    labels = [dates[i] for i in range(0, len(dates))  if i% 1 == 0]

    fig = plt.figure(figsize=(18,12))
    ax = fig.add_subplot(111)

    plt.xticks(np.arange(0,len(dates),1), labels)
    plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')

 
    ax.plot(dates, df['confirmed'],'o',label='confirmed',c='b')
    ax.plot(dates, df['tests'],'o',label='tests',c='y')
    ax.set_yscale('log')
    plt.legend()
    plt.grid()
    plt.show()
   

  
