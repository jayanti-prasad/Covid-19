import sys
import os
import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import common_utils as cu 
from epidemiology import  Epidemology 
from optimizer import Learner


def beta (b0, mu, t):
   return b0 * np.exp (-mu *t)

fcountries=['China','SK','Uruguay']

def get_fitting_data (args, df, country):

   df  = cu.get_country_data (df, country)
   df = df[df['confirmed'] > 100]

   dates = df['date'].to_list()
   data = df['confirmed'] - df['recovered'] - df['deaths']
   data.index = df['date'].to_list()
   #return data[start_date:]
   return data


def show_fitting(args, N, data, country_name, params):

   dates = list(data.index)
   days = [int(i) for i in range(0, data.shape[0])]

   dates_all = dates + cu.get_dates (dates[-1], 30)

   #  get the prediction 
   E = Epidemology (args.model_name,'solve_ivp',data.shape[0]+30)
   E.set_init(N, data[0], 0)
   sir = E.evolve (params)
  
   y_true = data.to_numpy()
   y_pred = sir.y[1,:][:y_true.shape[0]]

   mse  = np.sqrt(np.mean((y_true - y_pred)**2))

   title = country_name  + r', $\beta_0$' +"=" + str('%.2f' %params[0])\
      + r', $\mu$= ' +  str('%.2f' % params[1]) \
      + r', $\gamma$= '+ str('%.2f' % params[2])

   t = cu.strip_year(dates) 
   t_all = cu.strip_year(dates_all) 

   fig = plt.figure(figsize=(15,10))
   ax = fig.add_subplot(111)

   ax.plot(t_all,sir.y[1,:],c='r',label='Infected')
   ax.plot(t_all,sir.y[2,:],c='g',label='Recovered')
   plt.scatter(t, data.to_numpy(), c='b',label='Data')
   ax.set_yscale('log')
   ax.set_title(title)
   ax.legend()
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   plt.savefig(args.output_dir + os.sep +  country_name + ".pdf")
   #plt.show()
   return mse  

if __name__ == "__main__":
   """
   The main program 
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-m','--model-name',help='Model',default='dbsir')
   parser.add_argument('-o','--output-dir',help='Output directory')
   parser.add_argument('-n','--num-countries',type=int,\
      default=100, help='Number of countries')

   args = parser.parse_args()
   df = pd.read_csv(args.input_file)

   os.makedirs(args.output_dir, exist_ok=True)

   countries = cu.get_top_countries(df, args.num_countries)

   countries = [c for c in countries if c not in  fcountries]

   df_params = pd.DataFrame(columns=['country','beta_0','mu','gamma','R0','nmse'])
   count = 0
   #countries = ['Germany']

   for country in countries:
      try:
         data = get_fitting_data (args, df, country)
         N = cu.get_population(country)
         L = Learner(N, data, args.model_name)
         L.initial_guess()
         params = L.fit()
         #t = np.arange(0, data.shape[0],1)
         #print(t)
         #t_last = data.shape[0]
         #beta_t = [ beta (params[0], params[1], tt)/params[2] for tt in t]
         #plt.plot(t,beta_t)
         #plt.show()

         if params:
            R0 =  beta (params[0], params[1], data.shape[0])/params[2]
            mse = show_fitting(args, N, data, country, params)
            data_row = [country, "%.6f" % params[0],"%.6f" %params[1], "%.6f" % params[2],"%.6f" %R0, "%d" %mse]
            df_params.loc[count] = data_row 
            print(count, data_row)
            count +=1
      except:
         pass  
   df_params.to_csv(args.output_dir + os.sep + "best_fit_params.csv")

