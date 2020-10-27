import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime 
from pandas.plotting import lag_plot
from pandas.plotting import autocorrelation_plot

def get_dtobject  (date_str):
   print(date_str)
   parts = date_str.split('-')
   parts = [int(x) for x in parts]
   return datetime(parts[2], parts[0], parts[1], 0, 0, 0)

def plot_data (df):
   X = df['confirmed'] 
 
   fig = plt.figure(figsize=(18,8))
   ax = fig.add_subplot(111)
   #plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
   ax.plot(X,'.')
   plt.grid()
   plt.show()


def plot_lagplot(df):
   X = df['confirmed']
   lag_plot(X)
   plt.show()

def plot_autocorr(df):
   X = df['confirmed']
   autocorrelation_plot(X)
   plt.show()





if __name__ == "__main__":
 
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input file')  
   parser.add_argument('-c','--country-name',help='Input file')  
   
   args = parser.parse_args()

   dF = pd.read_csv(args.input_file)
   
   df = dF[dF['country'] == args.country_name]

   df.index = [get_dtobject(d) for d in df['date'].to_list()]
  
   df = df.sort_values(by='date')

   #plot_lagplot(df)
   plot_autocorr(df)
   #plot_data(df)



  


 
