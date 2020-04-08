import os
import sys
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import argparse 
import matplotlib

plt.rcParams.update({'font.size': 22})


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
   parser.add_argument('-s','--start-day',help='Starting day for  plot',\
      type=int,default=30)
   parser.add_argument('-e','--end-day',help='End day for  plot',\
      type=int,default=400)

   parser.add_argument('-o','--output-dir',help='Output dir',default='plots')

   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   df = pd.read_csv(args.input_file)
   df = df[df['country'] == args.country_name]
  
   start = args.start_day 
   end = args.end_day 

   print(df.shape, df.columns)
   df = df.fillna(0)

   D = {}
   for index, row in df.iterrows():
      D[row['date']] = [row['confirmed'], row['deaths'], row['recovered']]  

   dates = df['date'].to_list() 

   dates1 = [datetime.datetime.strptime(ts, "%m-%d-%Y") for ts in dates]
   dates2 = dates1.sort()

   x, yc, yd, yr = [], [], [], []  

   dfc = pd.DataFrame(columns=['date','confirmed','deaths','recovered'])
   count = 0 
   for d in dates1:
     dd = str(d).split()[0].split("-")
     key = dd[1]+"-"+dd[2]+"-"+dd[0]
     print(count, key, D[key]) 
     x.append(count)
     yc.append (D[key][0])
     yd.append (D[key][1])
     yr.append (D[key][2])
     dfc.loc[count] = [key,D[key][0], D[key][1], D[key][2]]
     count +=1

   dfc.to_csv(args.output_dir + os.sep + "cdr_" + args.country_name +".csv")

   dates1 = [str(x).replace('2020-','') for x in dates1]
   dates = [x.split(" ")[0] for x in dates1]

   fig  = plt.figure(figsize=(18,18))

   ax = fig.add_subplot(311)
   ax.set_title("Covid-19: "+args.country_name)
   plt.grid()
   ax.set_ylabel("Deaths")
   ax.set_xticklabels([])

   bx = fig.add_subplot(312)
   bx.set_ylabel("Recovered")
   bx.set_xticklabels([])
   plt.grid()

   cx = fig.add_subplot(313)
   plt.xticks(rotation=90)
   cx.set_ylabel("Infected")
   cx.tick_params(axis='x', which='major', labelsize=10)
   cx.tick_params(axis='x', which='minor', labelsize=8)

     
   ax.plot(dates[start:end], yd[start:end],'r',linewidth=4.0)
   bx.plot(dates[start:end], yr[start:end],'g',linewidth=4.0)
   cx.plot(dates[start:end], yc[start:end],'b',linewidth=4.0)
   plt.grid()
   plt.savefig(args.output_dir + os.sep + "cdr_" + args.country_name +".pdf")

