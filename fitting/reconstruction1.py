import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse 
import os 
from common_utils import get_country_data,strip_year
import numpy as np

class Reconstruct:
   def __init__(self, args):

      self.output_dir = args.output_dir  

      os.makedirs(self.output_dir, exist_ok=True)

      df = pd.read_csv(args.input_file)
      df_l = pd.read_csv(args.lockdown_file)

      # Get the country data 
      self.df = get_country_data (df, country)
      print("Country data frame:", self.df.shape)

      # Read the population and the lockdown date 
      population = dict(zip(df_l['country'].to_list(), df_l['population'].to_list()))
      L = dict(zip(df_l['country'].to_list(), strip_year(df_l['lockdown'].to_list())))

      self.lockdown = L[country]
      N = population[country]
  
      self.i = self.df['confirmed'].to_numpy()/N
      self.r = self.df['recovered'].to_numpy()/N
      self.d = self.df['deaths'].to_numpy()/N

      self.rr = np.zeros ([self.df.shape[0]]) # removed 
      self.s = np.zeros ([self.df.shape[0]])  # succeptable 
      self.e = np.zeros ([self.df.shape[0]])  # exposed 
      self.beta = np.zeros ([self.df.shape[0]]) # be


   def solve (self, gamma, sigma):

      # initial number for the removed 
      self.rr[0] = (self.r[0] + self.d[0])
   
      # Now get the reconstructed ones  
      for j in range(0, self.df.shape[0]-1):
         self.e[j] = (self.i[j+1] - self.i[j] + gamma * self.i[j])/sigma
         if j > 0:
            self.rr[j] = self.rr[j-1] + gamma * self.i[j-1]
         self.s[j] = 1.0 - (self.i[j] + self.e[j] + self.rr[j])

      for j in range(0, self.df.shape[0]-1):
         self.beta[j] = (self.e[j+1] - self.e[j] \
           + sigma * self.e[j])/ (self.s[j] * self.i[j])

      columns=['date','infected','exposed','removed','recovered','succeptable','beta']
      df_new = pd.DataFrame(columns=columns)
  
      df_new['date'] = self.df['date'].to_list()
      df_new['infected'] = self.i
      df_new['rcovered'] = self.r
      df_new['exposed'] = self.e
      df_new['removed'] = self.rr
      df_new['succeptable'] = self.s
      df_new['beta'] = self.beta

      return df_new 


def plot_data (args, df):

   dates = strip_year(df['date'].to_list())
   i = df['infected'].to_numpy()
   r = df['recovered'].to_numpy()
   rr = df['removed'].to_numpy()
   beta = df['beta'].to_numpy()
   e = df['exposed'].to_numpy()
   s = df['succeptable'].to_numpy()

   # Now draw the plot 
   fig = plt.figure(figsize=(12,12))
   ax  = fig.add_subplot(211)
   bx  = fig.add_subplot(212)

   ax.set_title(args.country_name)
   ax.plot(dates, beta)
   ax.plot(dates, beta,'o')
   ax.set_ylabel(r'$\beta(t)$')
   ax.axvline(x=self.lockdown)
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
   bx.axvline(x=self.lockdown)

   plt.savefig(args.output_dir + os.sep + args.country_name +".pdf")
   df_new.to_csv(args.output_dir + os.sep + args.country_name +".csv")

   print("Output csv file:", args.output_dir + os.sep + args.country_name +".csv")
   print("Output plot file:", args.output_dir + os.sep + args.country_name +".pdf")

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
   df_l = pd.read_csv(args.lockdown_file)

   R = Reconstruct(df, df_l, args.country_name)  

   df_new  = R.solve (args.gamma, args.sigma)
 
   plot_data (args, df_new)


