import os
import sys
import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common_utils import get_country_data,strip_year

"""
This is the newer version which has better flexibility to 
change sigma and gamma. 

"""

class Reconstruct:

   def __init__(self, args):
   
      """
      Read  input data and parse arguments.

      """
   
      self.country = args.country_name 

      self.output_dir = args.output_dir  
      os.makedirs(self.output_dir, exist_ok=True)

      df = pd.read_csv(args.input_file)
      df = df[df['confirmed'] > 25]

      df_l = pd.read_csv(args.lockdown_file)

      # Get the country data 
      self.df = get_country_data (df, self.country)
      print("Country data frame:", self.df.shape)
      self.num_rows = self.df.shape[0]       
 
      self.dates = strip_year(self.df['date'].to_list())

      # Read the population and the lockdown date 
      population = dict(zip(df_l['country'].to_list(), df_l['population'].to_list()))
      L = dict(zip(df_l['country'].to_list(), strip_year(df_l['lockdown'].to_list())))

      self.lockdown = L[self.country]
      N = population[self.country]
  
      self.i = self.df['confirmed'].to_numpy()/N
      self.r = self.df['recovered'].to_numpy()/N
      self.d = self.df['deaths'].to_numpy()/N

      self.rr = np.zeros ([self.num_rows]) # removed 
      self.s = np.zeros ([self.num_rows])  # succeptable 
      self.e = np.zeros ([self.num_rows])  # exposed 
      self.beta = np.zeros ([self.num_rows]) # be


   def solve (self, gamma, sigma):

      """
      SOLVE SEIR equations.  
      """

      self.gamma, self.sigma = gamma, sigma 

      prefix = '_sigma_%6.4f_gamma_%6.4f' % (sigma,gamma)
      self.prefix = self.country + prefix

      # initial number for the removed 
      self.rr[0] = (self.r[0] + self.d[0])
   
      # Now get the reconstructed ones  
      for j in range(0, self.num_rows-1):
         self.e[j] = (self.i[j+1] - self.i[j] + gamma * self.i[j])/sigma
         if j > 0:
            self.rr[j] = self.rr[j-1] + gamma * self.i[j-1]
         self.s[j] = 1.0 - (self.i[j] + self.e[j] + self.rr[j])

      for j in range(0, self.num_rows-1):
         self.beta[j] = (self.e[j+1] - self.e[j] \
           + sigma * self.e[j])/ (self.s[j] * self.i[j])

   def output (self):

      """
       Write output csv file and plot figure.
      """
      dates = self.dates 

      # Now draw the plot 
      fig = plt.figure(figsize=(12,12))
      ax  = fig.add_subplot(211)
      bx  = fig.add_subplot(212)

      ax.set_title(args.country_name + r'$, \gamma$='+str(self.gamma)+"," + r'$\sigma$='+ str(self.sigma))
      ax.plot(dates, self.beta)
      ax.plot(dates, self.beta,'o')
      ax.set_ylabel(r'$\beta(t)$')
      ax.axvline(x=self.lockdown,c='k',ls='--')
      plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
      ax.set_xlabel('t')

      bx.plot(dates,np.log(self.i),'b',label='Infected')
      bx.plot(dates,np.log(self.i),'o',c='blue')
      bx.plot(dates,np.log(self.r),'g',label='Recovered')
      bx.plot(dates,np.log(self.r),'o',c='green')
      bx.plot(dates,np.log(self.rr),'ro:',label='Removed')
      bx.plot(dates,np.log(self.e),'mo:',label='Exposed')
      bx.plot(dates,np.log(self.s),'k',label='Succeptable')
      plt.setp(bx.get_xticklabels(), rotation=90, horizontalalignment='right')
      bx.legend(loc='lower right')
      bx.axvline(x=self.lockdown,c='k',ls='--')
      plt.show()
      plt.savefig(self.output_dir + os.sep + self.prefix +".pdf")
      print("Output plot file:", self.output_dir + os.sep + self.country+".pdf")


      columns=['date','infected','exposed','removed','recovered','succeptable','beta']
      df_new = pd.DataFrame(columns=columns)

      df_new['date'] = self.df['date'].to_list()
      df_new['infected'] = self.i
      df_new['rcovered'] = self.r
      df_new['exposed'] = self.e
      df_new['removed'] = self.rr
      df_new['succeptable'] = self.s
      df_new['beta'] = self.beta

      df_new.to_csv(self.output_dir + os.sep + self.prefix +".csv")
      print("Output data file:",self.output_dir + os.sep + self.prefix +".csv")


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

   R = Reconstruct(args)

   R.solve (args.gamma, args.sigma)
 
   R.output ()



