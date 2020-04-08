import os
import sys
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import argparse 

"""
Plot the number of confirmed (c), deaths (d) and recovered (r)
case for the last given number of days for a given country. 

- Jayanti Prasad [prasad.jayanti@gmail.com]

"""

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-','--input-file',help='Input CSV file',\
      default='data/full-data-07-04-2020.csv')
   parser.add_argument('-c','--country-name',help='Country name',default='India')   
   parser.add_argument('-n','--num-days',help='Number of days to plot',\
      type=int,default=30)
   parser.add_argument('-o','--output-dir',help='Output dir',default='plots')

   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   df = pd.read_csv(args.input_file)
   df = df[df['country'] == args.country_name]
  
   n = args.num_days 

   print(df.shape, df.columns)
   df = df.fillna(0)

   D = {}
   for index, row in df.iterrows():
      D[row['date']] = [row['confirmed'], row['deaths'], row['recovered']]  

   dates = df['date'].to_list() 

   dates1 = [datetime.datetime.strptime(ts, "%m-%d-%Y") for ts in dates]
   dates2 = dates1.sort()

   x, yc, yd, yr = [], [], [], []  
   count = 0   
   for d in dates1:
     dd = str(d).split()[0].split("-")
     key = dd[1]+"-"+dd[2]+"-"+dd[0]
     print(count, key, D[key]) 
     x.append(count)
     yc.append (D[key][0])
     yd.append (D[key][1])
     yr.append (D[key][2])
     count +=1

   dates1 = [str(x).replace('2020-','') for x in dates1]
   dates = [x.split(" ")[0] for x in dates1]

   fig  = plt.figure(figsize=(12,12))

   ax = fig.add_subplot(311)
   ax.set_title("Deaths")
   plt.grid()
   ax.set_xticklabels([])


   bx = fig.add_subplot(312)
   bx.set_title("Recovered")
   bx.set_xticklabels([])
   plt.grid()

   cx = fig.add_subplot(313)
   plt.xticks(rotation=90)
   cx.set_title("Infected")
     
   ax.plot(dates[-n:], yd[-n:])
   bx.plot(dates[-n:], yr[-n:])
   cx.plot(dates[-n:], yc[-n:])
   plt.grid()
   plt.savefig(args.output_dir + os.sep + "cdr_" + args.country_name +".pdf")

