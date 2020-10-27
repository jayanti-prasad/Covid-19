import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from datetime import timedelta, date, datetime 

def get_dtobject  (date_str):
   parts = date_str.split('-')
   parts = [int(x) for x in parts]
   return datetime(parts[2], parts[0], parts[1], 0, 0, 0)


def get_future_dates (start_date, num_days):
   dates = []
   for i in range(1, num_days):
      tmp_date  = start_date + timedelta(days=i)
      dates.append(tmp_date)
   return dates


def predict(X,coeff,num_predict):
    ndata = len (X)
    nlags = len (coeff) -2 
    intercept = coeff[0]
    trend = coeff[1]
   
    k = 0
    while k < num_predict :
       y =  trend  
       for j in range (0, nlags):
          y +=coeff[2+j] * X[-nlags+j]
       tmp_date  = X.index[len(X)-1]  + timedelta(days=1)
       dX = pd.Series([y for i in range (0,1)])
       dX.index = [tmp_date]
       print(k, dX)
       X = pd.concat ([X, dX]) 
       k +=1
    return X 


if __name__ == "__main__":
 
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input file')  
   parser.add_argument('-c','--country-name',help='Input file')  
   parser.add_argument('-l','--lag-time',type=int,help='Lag days',default=7)  
   
   args = parser.parse_args()

   dF = pd.read_csv(args.input_file)
   
   df = dF[dF['country'] == args.country_name]
   df.index = [get_dtobject(d) for d in df['date'].to_list()]
   df = df.sort_values(by='date')

   X = df['confirmed']

   train, test = X.iloc[1:len(X)-args.lag_time], X.iloc[len(X)-args.lag_time:]

   # train autoregression
   model = AutoReg(train, lags=args.lag_time,trend='ct')
   model_fit = model.fit()
   print('Coefficients: %s' % model_fit.params)

   coeff =  model_fit.params

   Y = predict(X,coeff,7)

   fig = plt.figure(figsize=(12,6))
   ax = fig.add_subplot(111)
   ax.plot(X.iloc[-30:],'o',label='True')
   ax.plot(Y.iloc[-40:], color='red',label='Predicted')
   plt.grid()
   plt.legend()
   plt.show()
   
