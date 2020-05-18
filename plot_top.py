import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from common_utils import date_normalize,get_country_data,get_date_diff 
import matplotlib 
import numpy as np

fontsize = 8
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)

def get_top_countries(df, count):
    df = df.replace({'United Kingdom': 'UK'}, regex=True)
    df1 = df.copy()
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0]
    df_top = df1[df1['date'] == last_date]
    df_top = df_top.sort_values(by=['confirmed'],ascending=False)[:count]

    return df_top  


if __name__ == "__main__":

   df = pd.read_csv(sys.argv[1])
   df_l = pd.read_csv("data/lockdown.csv")
 
   L = df_l['date']
   L.index = df_l['country'].to_list()


   df_top = get_top_countries(df, 100)
   x = [int(i) for i in range(0, 500)] 
   y = df_top['confirmed'].to_list()

   countries = df_top['country'].to_list()

   with open ("/Users/jayanti/Projects/Softlab/Covid-19/code/output/17-05-2020/bad_fit.txt","r") as fp:
      data = fp.read()

   countries=data.split('\n')

   #print(countries)
   #sys.exit()  
 
   fig = plt.figure(figsize=(12,18))
   col = 1
   for c in countries:
      try:
        dF = get_country_data (df, c)
      except:
        continue  

      x = [int(i) for i in range(0, dF.shape[0])]
      x = dF['date'].to_list()
      y = dF['confirmed'] -dF['deaths'] -dF['recovered']
      if dF.shape[0] > 0 and col < 51 and c != 'China':
         #lockdown_day = np.max (get_date_diff(dF.iloc[0]['date'], L[c]),0) 
         print(c,dF.shape,dF.iloc[0]['date'])
         ax = fig.add_subplot(10,5,col)
         #fig = plt.figure(figsize=(18,12))
         #ax = fig.add_subplot(1,1,1)
         #plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
         #ax.axvline(x=float(lockdown_day),c='k',ls='--')
         ax.plot(x,y,'b')
         #ax.plot(x,y,'bo')
         ax.set_title(c, fontsize=fontsize)
         #ax.set_yscale('log')
         #ax.grid()
         ax.set_xticks([])
         ax.set_yticks([])
         col +=1
         #plt.show()
         #plt.savefig("tests1" + os.sep + c + ".png") 

   #plt.savefig("plots" + os.sep +"top50a.pdf") 
   plt.show()

