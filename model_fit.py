import os
import sys
import argparse
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from models import ExpModel, TimeSeriesModel  
from common_utils import date_normalize, get_dates, strip_year 


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input csv file')
   parser.add_argument('-c', '--country', help='Country',default='India')
   parser.add_argument('-s', '--start-day', help='Star day for fitting data',type=int,default=10)
   parser.add_argument('-e', '--end-day', help='End day for fitting data', type=int,default=80)
   parser.add_argument('-n', '--num-predict', help='Number of days to predict', type=int,default=10)
   parser.add_argument('-o', '--output-dir', help='Output dir',default="plots")
   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   # read and normalize the data frame 
   df = pd.read_csv(args.input_file)
   df = df.fillna(0)
   df = df[df['country'] == args.country]

   df = date_normalize (df)
   df = df.sort_values(by='dates')
 
   print("day-date-confirmed-recovered-deaths")
   count = 0
   for index,row in df.iterrows():
      print(count, row['date'], row['confirmed'], row['recovered'], row['deaths'])
      count +=1


   # let us get all the dates 
   dates = df['dates'].to_list() 

   # add some future dates also 
   dates_predict = dates + get_dates (dates[df.shape[0]-1],args.num_predict)

   # get the days
   days = np.array([float(i) for i in range(0, len(dates))])
   days_predict  = np.array([float(i) for i in range(0, len(dates_predict))])


   # let us get rid of the year for plotting 
   dates_predict = strip_year (dates_predict)
   dates = strip_year (dates)

   # now let us iterate over the three columns 
   cases=["deaths","recovered","confirmed"]

   fig = plt.figure(figsize=(18,18))

   ax = [plt.subplot(311)]
   ax.append(plt.subplot(312))
   ax.append(plt.subplot(313))

   num_days = len(days)

   for i in range(0, len(cases)):
      y = df[cases[i]].to_numpy()
      ax[i].plot(dates,y, 'bo',label='Full data' )
      plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
      ax[i].set_ylabel(cases[i])
      ax[i].grid()

      if i < 2 :
         ax[i].set_xticklabels([])
      if i == 0: 
         ax[i].set_title("Covid-19: " + args.country)

      model = ExpModel()
      model.fit(days,y)          
      y_predict = model.predict(days_predict)

      model1 = TimeSeriesModel(5)
      model1.fit (days[model.start:],y[model.start:])

      y_predict1 = model1.predict(y[-10], 10 + args.num_predict)     

      days_predict1 = dates_predict[num_days-10:num_days+args.num_predict] 

      ax[i].plot(days_predict1, y_predict1, 'r-',\
         label='fit: growth rate =%5.3f ' % (model1.rate))

      ax[i].plot(dates_predict[model.start:], y_predict[model.start:], 'k-',\
         label='fit [a*exp(-b)]: a=%5.3f, b=%5.3f' % (model.a,model.b))

      ax[i].legend()

   plt.savefig(args.output_dir + os.sep + args.country + "_model_fit.pdf")
   plt.show()
