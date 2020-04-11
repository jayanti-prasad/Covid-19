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
   parser.add_argument('-o', '--output-dir', help='Output dir',default="plots")
   parser.add_argument('-c', '--country', help='Country',default='India')
   parser.add_argument('-t', '--type', help='Data colums',default="confirmed")
   parser.add_argument('-s', '--start-day', help='Start day',default=0,type=int)
   parser.add_argument('-e', '--end-day', help='End day',default=0,type=int)
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
   end = args.end_day 

   for i in range (0, df.shape[0]):
      if start == 0 and y[i] > 0:
          start = i

   if end == 0:
      end = df.shape[0]

   x = np.array(x[start:end] - x[start]) 
   y = np.log(y[start:end])

   slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
   y_predict = intercept + slope * x 
   x = strip_year(dates[start:end])

   parts1 = dates[start].split("-")
   parts2 = dates[end-1].split("-")
   p1 = parts1[2]+"-"+parts1[1]+"-"+parts1[0]
   p2 = parts2[2]+"-"+parts2[1]+"-"+parts2[0]

   #date_str = dates[start]+"_to_"+dates[end-1]
   date_str = p1 +"_to_"+p2

   output_file = args.output_dir + os.sep + args.country+"_"+args.type+"_"+date_str+".pdf"

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
   plt.savefig(output_file)
   print("output file:", output_file)
