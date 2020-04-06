import os
import sys
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib 
import numpy as np
import argparse
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 
matplotlib.pyplot.grid(True, which="both")

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input CSV file')
   parser.add_argument('-o', '--output-dir', help='Output dir')
   parser.add_argument('-c', '--country', help='Country')
   parser.add_argument('-d', '--num-days', type=int, help='Number of days', default=30)
   args = parser.parse_args()

   df = pd.read_csv(args.input_file)
   os.makedirs(args.output_dir, exist_ok=True)

   print("Latest data point")
   print("data:",df.columns)
   print("columns:",df.columns)

   date_column= 'ObservationDate'
   country_column ='Country/Region'
   deaths_column = 'Deaths' 

   if args.country not in list(set(df[country_column].to_list())):
      print("Give the country name from the following:\n")
      print(list(set(df[country_column].to_list())))
      sys.exit() 

   df_c = df[df[country_column] == args.country]
   dates = df_c[date_column].to_list()
   dates = [x.replace('/2020','') for x in dates]
   y_c = df_c[deaths_column].to_list()
 
   y =  [0] + [ y_c[i]-y_c[i-1]  for i in range (1, len(y_c))]

   fig,ax = plt.subplots(figsize=(20, 10))
   start = -1 * args.num_days 

   plt.plot(dates[start:], y[start:],label='Number of death')
   plt.plot(dates[start:], y[start:],'o')
   plt.plot(dates[start:], y_c[start:],label='Number of death till date')
   plt.plot(dates[start:], y_c[start:],'o')

   plt.xticks(rotation=90)
   plt.ylabel("Total deaths")
   plt.title(args.country)
   plt.grid()
   ax.legend()
   plt.savefig(args.output_dir  + os.sep + args.country +".pdf")
