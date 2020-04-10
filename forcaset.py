import os
import sys
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd 
import argparse
from common_utils import date_normalize

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i', '--input-file', help='Input csv file')
   parser.add_argument('-c', '--country', help='Country',default='India')
   parser.add_argument('-o', '--output-dir', help='Output dir',default="plots")
   parser.add_argument('-l','--log',help='Log option',action='store_true')
   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   df = pd.read_csv(args.input_file)
   df = df[df['country'] == args.country]

   df = date_normalize (df)
   df = df.sort_values(by='dates')
   
   dates = [d.replace('2020-','') for d in df['dates'].to_list()]

   x = np.array([float(i) for i in range(0, len(dates))])

   y = df['confirmed'].to_numpy()
   print("data size:", y.shape)

   #if args.log:
   #   plt.plot(x,np.log10(y),'o')
   #else:
   #   plt.plot(x,y,'o')

   g = np.mean([y[i+1]/y[i] for i in range(10,60)])
   print(g)

   y_p = y.item(58)

   for i in range(58, 68):
      y_p = y_p *(1.0+g)
      print(i+58, y_p,y[i])



   plt.show()
