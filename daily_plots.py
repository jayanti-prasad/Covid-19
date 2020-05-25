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

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='data/covid-19-global.csv')
    parser.add_argument('-c','--country',help='Country name',default='India')
    parser.add_argument('-o','--output-dir',help='Output dir',default='current')

    args = parser.parse_args()
    countries_dir = args.output_dir + os.sep + "data"
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(countries_dir, exist_ok=True)

    dF = pd.read_csv(args.input_file)
    df = get_country_data (dF, args.country)
    df.index = df['date'].to_list() 

    #dF1 = pd.read_csv("data/owid-covid-data.csv")
    #df1 = get_country_data_owid (dF1, args.country)

    #dF2 = pd.read_csv("data/kaggel/covid_19_data.csv")
    #df2 = get_country_data_kaggle (dF2, args.country)

    #print(df2.index)

    #sys.exit()

    #df1 = df1[df1.index.isin(df.index)]
    #dates1 = strip_year(df1['date'].to_list())

    #df2 = df2[df2.index.isin(df.index)]
    #dates2 = strip_year(df2['date'].to_list())

    dates = strip_year (df['date'].to_list())
    days  = [int(i) for i in range(0, len(dates))]

    fig = plt.figure(figsize=(18,18))
 
    ax = [fig.add_subplot(311)]  
    ax.append(fig.add_subplot(312))  
    ax.append(fig.add_subplot(313))

    cases = ['confirmed','recovered','deaths']  
    colors = ['blue','green','red']

    #print(df1.shape, df2.shape, df.shape)
    #print(df1.columns, df2.columns, df.columns)
    #print(dates)
    #print(dates1)
    #print(dates2)

    #sys.exit()


    for i in range (0, len(cases)):

       
      Y = df[cases[i]]
      #Y2 = df2[cases[i]]


      #Y.index = dates 

      labels = [dates[i] for i in range(0, len(days))  if i% 3 == 0]
      plt.xticks(np.arange(0,len(days),3), labels)
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')

      #dY = Y.diff(periods=1).iloc[1:]
      #ax[i].plot(dates[1:], dY,c=colors[i])
      #ax[i].scatter(dates[1:], dY,c=colors[i])

      ax[i].plot(dates, Y,c=colors[i])
      ax[i].scatter(dates, Y,c=colors[i])
  
      #ax[i].plot(dates2, Y2,'+',c='k')


      #if i != 1:
      #   X = df1[cases[i]]
      #   ax[i].plot(dates1, X,'x',c='y')

      ax[i].set_ylabel(cases[i])
      ax[i].grid()

      if i == 0:
        ax[i].set_title(args.country)
      if i < 2 :
        ax[i].set_xticklabels([])

    plt.savefig(args.output_dir + os.sep + "covid-19-"+args.country+".pdf")
    plt.show()
  
