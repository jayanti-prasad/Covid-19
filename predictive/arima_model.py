import pandas as pd
import matplotlib.pylab as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import argparse
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from datetime import datetime 
plt.style.use('ggplot')


months = {'January':'1', 'February':'2', 'March':'3', 'April':'4', 'May':'5', 'June':'6',\
    'July':'7','August':'8', 'September':'9', 'October':'10', 'November':'11', 'December':'12'}

def format_data (date_str):
   parts = date_str.split("-")
   date = datetime(int(parts[2]), int(months[parts[1]]), int(parts[0]), 0, 0, 0)
   return date 


def plot_data (X):

   fig = plt.figure(figsize=(12,6))
   ax = fig.add_subplot(111)
   ax.plot(X,'o')
   plt.show()
  

if __name__ == "__main__":
   
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input File')
   window = 24

 
   args = parser.parse_args()

   df = pd.read_csv(args.input_file) 
   
   print(df.shape, df.columns)

   df['Date'] = [format_data(d) for d in df['Date'].to_list()] 
   df.index =   df['Date'].to_list()
   df = df.sort_values(by='Date')

   #plot_data(df['Open Price'])

   X = df['Open Price']

   decomposed = seasonal_decompose(X,freq = 12)

   x = decomposed.plot() #See note below about this 
   plt.rcParams['figure.figsize']=(35,15)
   plt.style.use('ggplot')
   plt.show()


   df['stationary']=df['Open Price'].diff()
   X = df['stationary'].dropna()
   train_data = X.iloc[1:len(X)-window]
   test_data = X.iloc[X[len(X)-window:]]

   #train the autoregression model
   model = AR(train_data)
   model_fitted = model.fit()

   model_fitted  = ARMA(train_data, order=(0, 1)).fit()
   #y_mam = ma.predict(190,247)
   #y_mam.index = y_test.index
   #mse(y_mam,y_test)

   print('The lag value chose is: %s' % model_fitted.k_ar)
   print('The coefficients of the model are:\n %s' % model_fitted.params)
  
   # make predictions 
   predictions = model_fitted.predict(start=len(train_data),\
      end=len(train_data) + len(test_data)-1, dynamic=False)
   predictions.index = X.index[len(X)-window:]


   compare_df = pd.concat([df['stationary'].tail(window),predictions],\
      axis=1).rename(columns={'stationary': 'actual', 0:'predicted'})

   #plot the two values
   plt.plot(compare_df['actual'],label='Actual')
   plt.plot(compare_df['predicted'],label='Predicted')
   plt.legend()
   plt.show()



