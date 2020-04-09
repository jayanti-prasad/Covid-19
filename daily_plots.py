import os
import sys
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import argparse 
import matplotlib

plt.rcParams.update({'font.size': 12})


"""
Plot the number of confirmed (c), deaths (d) and recovered (r)
case for the last given number of days for a given country. 

- Jayanti Prasad [prasad.jayanti@gmail.com]

"""

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-','--input-file',help='Input CSV file',\
      default='data/covid-19-data-latest.csv')
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

   xx = []
   yy = np.zeros([df.shape[0],3])

   dfc = pd.DataFrame(columns=['date','confirmed','deaths','recovered'])
   count = 0 
   for d in dates1:
     dd = str(d).split()[0].split("-")
     key = dd[1]+"-"+dd[2]+"-"+dd[0]
     xx.append(key)
     yy[count, 2] = D[key][0] 
     yy[count, 0] = D[key][1] 
     yy[count, 1] = D[key][2] 
     dfc.loc[count]=[key,D[key][0],D[key][1],D[key][2]]
     count +=1
   
   dfc.to_csv("data" + os.sep + args.country_name +".csv")
   print("Output written:", "data" + os.sep + args.country_name +".csv")
 
   dates1 = [str(x).replace('2020-','') for x in dates1]
   dates = [x.split(" ")[0] for x in dates1]

   cases=['deaths','recovered','confirmed']
   colors=['red','green','blue']
   fig  = plt.figure(figsize=(18,18))
   ax = []

   ax.append(fig.add_subplot(311))
   ax.append(fig.add_subplot(312))
   ax.append(fig.add_subplot(313))

   for i in range(0, len(cases)):
      plt.xticks(rotation=90)
      ax[i].plot(dates[start:end], yy[start:end,i],'r',linewidth=4.0,c=colors[i])
      ax[i].set_ylabel(cases[i])
      ax[i].tick_params(labeltop=False, labelright=True)
      if i == 0:
         ax[i].set_title(args.country_name)
      if i < 2:
        ax[i].set_xticklabels([])
      else :
        ax[i].tick_params(axis='x', which='major', labelsize=10)
        ax[i].tick_params(axis='x', which='minor', labelsize=8)
      ax[i].grid()
 

   plt.savefig(args.output_dir + os.sep + args.country_name +".pdf")
   print("Input file:",args.input_file)
   print("Output file:",args.output_dir + os.sep + args.country_name +".pdf")
