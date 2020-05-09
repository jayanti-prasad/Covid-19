import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import argparse 
import datetime
from common_utils import date_normalize, get_country_data
from datetime import date

"""
Plot daily time series data for a country. 

"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='data/covid-19-global.csv')
    parser.add_argument('-c','--country',help='Country name',default='India')
    parser.add_argument('-o','--output-dir',help='Output dir',default='daily_updates')
    parser.add_argument('-n','--num-days',help='Number of days',default=0,type=int)

    args = parser.parse_args()

    countries_dir = args.output_dir + os.sep + "data"
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(countries_dir, exist_ok=True)

    df = pd.read_csv(args.input_file)
    
    if args.country not in df['country'].to_list():
       print("countries:",df['country'].to_list())

    df = get_country_data (df, args.country)

    df.to_csv(countries_dir + os.sep  + "covid-19-"+args.country + ".csv",index=False)

    dates = [d.replace('2020-','') for d in df['date'].to_list()]
    days  = [int(i) for i in range(0, len(dates))]

    print("dates:",dates)

    fig = plt.figure(figsize=(18,18))
 
    ax = [fig.add_subplot(311)]  
    ax.append(fig.add_subplot(312))  
    ax.append(fig.add_subplot(313))

    cases = ['deaths','recovered','confirmed']  
    colors = ['red','green','blue']

    for i in range (0, len(cases)):
      #plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
      y = df[cases[i]].to_numpy()
      #ax[i].plot(dates,y,c=colors[i])

      labels = [dates[i] for i in range(0, len(days))  if i% 3 == 0]
      plt.xticks(np.arange(0,len(days),3), labels)
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')

      ax[i].plot(dates[-1*args.num_days:],y[-1*args.num_days:],c=colors[i])
      ax[i].scatter(dates[-1*args.num_days:],y[-1*args.num_days:],c=colors[i])
      ax[i].set_ylabel(cases[i])
      #ax[i].grid()
      #if i == 0:
      #  ax[i].set_title(args.country)
      #if i < 2 :
      #  ax[i].set_xticklabels([])

    plt.savefig(args.output_dir + os.sep + "covid-19-"+args.country+".pdf")
    plt.show()
  
