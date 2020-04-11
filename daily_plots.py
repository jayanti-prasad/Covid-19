import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import argparse 
import datetime
from common_utils import date_normalize

"""
Plot daily time series data for a country. 

"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='data/covid-19-data-latest.csv')
    parser.add_argument('-c','--country',help='Country name',default='India')
    parser.add_argument('-o','--output-dir',help='Output dir',default='plots')
    parser.add_argument('-n','--num-days',help='Number of days',default=0,type=int)

    args = parser.parse_args()

    df = pd.read_csv(args.input_file)
    df = df[df['country'] == args.country]

    df = date_normalize (df)
    df = df.sort_values(by='date') 

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('country')]

    df.to_csv("data/"+args.country + ".csv",index=False)

    dates = [d.replace('2020-','') for d in df['date'].to_list()]

    print("dates:",dates)

    fig = plt.figure(figsize=(18,18))
 
    ax = [fig.add_subplot(311)]  
    ax.append(fig.add_subplot(312))  
    ax.append(fig.add_subplot(313))

    cases = ['deaths','recovered','confirmed']  
    colors = ['red','green','blue']

    for i in range (0, len(cases)):
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
      y = df[cases[i]].to_numpy()
      ax[i].plot(dates,y,c=colors[i])
      #ax[i].scatter(dates[-1*args.num_days:],y[-1*args.num_days:],'o')
      ax[i].set_ylabel(cases[i])
      ax[i].grid()
      if i == 0:
        ax[i].set_title(args.country)
      if i < 2 :
        ax[i].set_xticklabels([])

    plt.savefig(args.output_dir + os.sep + args.country+".pdf")

 
