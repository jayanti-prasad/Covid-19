import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from models import ExpModel, TimeSeriesModel
from common_utils import date_normalize, get_dates, strip_year
from scipy import stats

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input csv file')
   parser.add_argument('-c', '--country', help='Country',default='India')
   parser.add_argument('-t', '--type', help='Data colums',default="confirmed")
   parser.add_argument('-s', '--start-day', help='Start day',default=0,type=int)
   args = parser.parse_args()

   # read and normalize the data frame 
   df = pd.read_csv(args.input_file)
   df = df.fillna(0)
   df = df[df['country'] == args.country]

   df = date_normalize (df)
   df = df.sort_values(by='dates')
   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]

   x = np.array([float(i) for i in range(0, df.shape[0])]) 
   y = df[args.type].to_numpy()
   dates = df['dates'].to_list()
   
   count = 0 
   print("day-date-confirmed-recovered-deaths")
   for index, row in df.iterrows():
      print(count, row['date'], row['confirmed'], row['recovered'],row['deaths'])
      count +=1

 
   start = args.start_day
   for i in range (0, df.shape[0]):
      if start == 0 and y[i] > 0:
          start = i

   x = x[start:] - x[start] 
   y = np.log(y[start:])

   slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
   y_predict = intercept + slope * x 

   x = strip_year(dates[start:])

   fig = plt.figure()
   ax = fig.add_subplot()

   ax.set_title(args.type)
   ax.plot(x,y,'o',label='data')
   ax.plot(x,y_predict)
   ax.plot(x, y_predict,'k-',\
      label='fit [y = a + b *x]: a=%5.3f, b=%5.3f' % (intercept,slope))
   ax.legend()
   ax.set_ylabel("log( "+args.type+" )")
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   plt.savefig("plots" + os.sep + args.country+"_"+args.type+".pdf")
 
