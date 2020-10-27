import argparse
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.seasonal import seasonal_decompose
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
  

def get_reg_data (dfr,p):

   print(dfr.shape)
   for i in range(1,p+1):
      df_temp['Shifted_values_%d' % i ] = df_temp['Value'].shift(i)



if __name__ == "__main__":
   
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input File')
   parser.add_argument('-k','--reg-order',type=int,help='Regression Order')
   window = 24

   args = parser.parse_args()

   df = pd.read_csv(args.input_file) 
   
   print(df.shape, df.columns)

   df['Date'] = [format_data(d) for d in df['Date'].to_list()] 
   df.index =   df['Date'].to_list()
   df = df.sort_values(by='Date')

   df_reg = get_reg_data (df[['Open Price']].copy())




