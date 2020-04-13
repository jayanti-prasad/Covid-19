import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse 
import os 
from common_utils import get_country_data,strip_year
import numpy as np


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country name', default='India')
   parser.add_argument('-o','--output-dir',help='Output dir', default='plots') 
   parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')

   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   print("parameters:", vars(args))

   df = pd.read_csv(args.input_file)
   df = get_country_data (df, args.country_name)

   # read the lockdown file 
   df_l = pd.read_csv(args.lockdown_file)

   N = dict(zip(df_l['country'].to_list(), df_l['population'].to_list())) 
   L = dict(zip(df_l['country'].to_list(), strip_year(df_l['lockdown'].to_list())))

   print("Population=",N[args.country_name])
   print("Lockdown=",L[args.country_name])

   df = df[df['confirmed'] > 25]
   print("data frame after removing low count:",df.shape)

   days = [int(i) for i in range(0, df.shape[0])]
   dates = strip_year(df['date'].to_list())
   
   count = 0 

   i = np.zeros ([df.shape[0]])
   r = np.zeros ([df.shape[0]])
   rr = np.zeros ([df.shape[0]])
   s = np.zeros ([df.shape[0]])
   e = np.zeros ([df.shape[0]])
   beta = np.zeros ([df.shape[0]])

   population = N[args.country_name]
   gamma = 1.0/7.0
   sigma = 1.0/7.0

   count = 0 
   for index, row in df.iterrows():
      i[count] = row['confirmed']/population 
      rr[count] = row['recovered']/population 
      count +=1
  
   for j in range(1, df.shape[0]):   
      e[j] = ( i[j] - i[j-1] + gamma * i[j])/sigma 
      r[j] = r[j-1] + gamma * i[j] 
      s[j] = 1.0 - ( i[j] + e[j] + r[j])
      beta[j] = (e[j] - e[j-1] + sigma * e[j])/ (s[j] * i[j])

   
   columns=['date','infected','exposed','recovered','succeptable','beta']
   df_new = pd.DataFrame(columns=columns)
   df_new['date'] = df['date'].to_list()
   df_new['infected'] = i
   df_new['exposed'] = e
   df_new['recovered'] = rr
   df_new['succeptable'] = s
   df_new['beta'] = beta

   df_new.to_csv(args.output_dir + os.sep + args.country_name +".csv")

   fig = plt.figure(figsize=(12,12))
   ax  = fig.add_subplot(211)
   bx  = fig.add_subplot(212)

   ax.plot(dates, beta)
   ax.plot(dates, beta,'o')
   ax.set_ylabel(r'$\beta(t)$')
   ax.axvline(x=L[args.country_name])
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   ax.set_xlabel('t')

   bx.plot(dates,np.log(i),label='Infected')
   bx.plot(dates,np.log(e),':',label='Exposed')
   bx.plot(dates,np.log(r),':',label='Removed')
   bx.plot(dates,np.log(rr),label='Removed+Dead')
   bx.plot(dates,np.log(s),label='Succeptable')
   plt.setp(bx.get_xticklabels(), rotation=90, horizontalalignment='right')
   bx.legend() 
   bx.axvline(x=L[args.country_name])
   plt.savefig(args.output_dir + os.sep + args.country_name +".pdf")

