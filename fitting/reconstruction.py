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
   parser.add_argument('-g','--gamma',help='Parameter gama',type=float,default=0.142857)
   parser.add_argument('-s','--sigma',help='Parameter sigma',type=float,default=0.142857)
   parser.add_argument('-o','--output-dir',help='Output dir', default='results') 
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

   # This is the condition we have imposed 
   df = df[df['confirmed'] > 25]
   print("data frame after removing low count:",df.shape)

   days = [int(i) for i in range(0, df.shape[0])]
   dates = strip_year(df['date'].to_list())
   
   count = 0 

   # These three are directly avaliable from the data 
   i = np.zeros ([df.shape[0]]) # infected
   r = np.zeros ([df.shape[0]]) # recovered
   d = np.zeros ([df.shape[0]]) # dead


   rr = np.zeros ([df.shape[0]]) # removed 
   s = np.zeros ([df.shape[0]])  # succeptable 
   e = np.zeros ([df.shape[0]])  # exposed 
   beta = np.zeros ([df.shape[0]]) # beta 

   population = N[args.country_name]
   # read from data file 

   gamma = args.gamma # can be given (default=1/7)
   sigma = args.sigma # can be given (default=1/7)

   # Let us read what is available  
   count = 0 
   for index, row in df.iterrows():
      i[count] = row['confirmed']/population 
      r[count] = row['recovered']/population 
      d[count] = row['deaths']/population 
      count +=1
  
   # initial number for the removed 
   rr[0] = (r[0]+d[0])
   
   # Now get the reconstructed ones  
   for j in range(0, df.shape[0]-1):   
      e[j] = (i[j+1] - i[j] + gamma * i[j])/sigma 
      if j > 0:
         rr[j] = rr[j-1] + gamma * i[j-1] 
      s[j] = 1.0 - (i[j] + e[j] + rr[j])

   for j in range(0, df.shape[0]-1):   
      beta[j] = (e[j+1] - e[j] + sigma * e[j])/ (s[j] * i[j])
    



   # For writing the data in a file (csv)
   columns=['date','infected','exposed','removed','succeptable','beta']
   df_new = pd.DataFrame(columns=columns)
   df_new['date'] = df['date'].to_list()
   df_new['infected'] = i
   df_new['exposed'] = e
   df_new['removed'] = rr
   df_new['succeptable'] = s
   df_new['beta'] = beta
   df_new.to_csv(args.output_dir + os.sep + args.country_name +".csv")

   # Now draw the plot 
   fig = plt.figure(figsize=(12,12))
   ax  = fig.add_subplot(211)
   bx  = fig.add_subplot(212)

   ax.set_title(args.country_name)
   ax.plot(dates, beta)
   ax.plot(dates, beta,'o')
   ax.set_ylabel(r'$\beta(t)$')
   ax.axvline(x=L[args.country_name])
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   ax.set_xlabel('t')

   bx.plot(dates,np.log(i),'b',label='Infected')
   bx.plot(dates,np.log(i),'o',c='blue')
   bx.plot(dates,np.log(r),'g',label='Recovered')
   bx.plot(dates,np.log(r),'o',c='green')
   bx.plot(dates,np.log(rr),'ro:',label='Removed')
   bx.plot(dates,np.log(e),'ko:',label='Exposed')
   #bx.plot(dates,np.log(s),'k',label='Succeptable')
   plt.setp(bx.get_xticklabels(), rotation=90, horizontalalignment='right')
   bx.legend(loc='lower right') 
   bx.axvline(x=L[args.country_name])
   plt.savefig(args.output_dir + os.sep + args.country_name +".pdf")

