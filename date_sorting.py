import os
import sys
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

   df = pd.read_csv(sys.argv[1])
   # input file : data/full-data-07-04-2020.csv 
   df = df[df['country'] == sys.argv[2]]
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

   fig  = plt.figure(figsize=(12,4))

   ax = fig.add_subplot(131)
   ax.set_title("Confirmed")
   plt.grid()

   bx = fig.add_subplot(132)
   bx.set_title("Deaths")
   plt.grid()

   cx = fig.add_subplot(133)
   cx.set_title("Recovered")
     
   ax.plot(x, yc)
   bx.plot(x, yd)
   cx.plot(x, yr)
   plt.grid()
   plt.savefig("plots" + os.sep + "cdr_" + sys.argv[2]+".pdf")



