import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import argparse 
import datetime
from common_utils import date_normalize
from datetime import date

"""
Plot daily time series data for a country. 

"""

def get_top_countries (args, df):
    df1 = df.copy() 
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0] 
    df_last = df1[df1['date'] == last_date]
    df_last = df_last.sort_values(by=['deaths'],ascending=False)[:10]

    fig = plt.figure (figsize=(12,18))
    ax = fig.add_subplot(111)

    df_last.plot(x="country", y="confirmed", kind="bar", ax=ax, color="C1")
    df_last.plot(x="country", y="recovered", kind="bar", ax=ax, color="C2")
    df_last.plot(x="country", y="deaths", kind="bar", ax=ax, color="C3")
    ax.set_yscale('log')
    ax.set_title("Covid-19:" + str(date.today()))
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right',fontsize=10)
    plt.savefig(args.output_dir + os.sep+ "top_countries.pdf")
    #plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file',\
      default='data/covid-19-global.csv')
    parser.add_argument('-c','--country',help='Country name',default='India')
    parser.add_argument('-o','--output-dir',help='Output dir',default='plots')
    parser.add_argument('-n','--num-days',help='Number of days',default=0,type=int)

    args = parser.parse_args()

    countries_dir = args.output_dir + os.sep + "data"
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(countries_dir, exist_ok=True)

    df = pd.read_csv(args.input_file)
    
    if args.country not in df['country'].to_list():
       print("countries:",df['country'].to_list())

    df = df.replace({'United Kingdom': 'UK'}, regex=True)
  
    get_top_countries (args, df)
    #sys.exit()

    df = df[df['country'] == args.country]

    df = date_normalize (df)
    df = df.sort_values(by='date') 

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('country')]

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
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
      y = df[cases[i]].to_numpy()
      #ax[i].plot(dates,y,c=colors[i])
      ax[i].plot(dates[-1*args.num_days:],y[-1*args.num_days:],c=colors[i])
      ax[i].scatter(dates[-1*args.num_days:],y[-1*args.num_days:],c=colors[i])
      ax[i].set_ylabel(cases[i])
      ax[i].grid()
      if i == 0:
        ax[i].set_title(args.country)
      if i < 2 :
        ax[i].set_xticklabels([])

    plt.savefig(args.output_dir + os.sep + "covid-19-"+args.country+".pdf")
    plt.show()
  
