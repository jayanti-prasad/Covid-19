import sys
import os
import argparse 
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from common_utils import get_country_data, date_normalize,country_normalize 
from epidemiology import SIR, SEIR, SEIARD, Epidemology 
from optimizer import Learner 

def get_top_countries(df, count):
    df = country_normalize(df)
    df1 = df.copy()
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0]
    df_top = df1[df1['date'] == last_date]
    df_top = df_top.sort_values(by=['confirmed'],ascending=False)[:count]
  
    return df_top['country'].to_list()

if __name__ == "__main__":
   """
   The main program 
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country Name')
   parser.add_argument('-p','--population-file',help='Country population file',default='../data/world_population.csv')
   parser.add_argument('-m','--model-name',help='Model',default='sir')

   args = parser.parse_args()
   df = pd.read_csv(args.input_file)

   df_p = pd.read_csv(args.population_file)
   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()

   countries = get_top_countries(df, 50)

   print("countries:",countries)

   df_params = pd.DataFrame(columns=['country','beta','mu','gamma'])
   count = 0
   for country in countries:
      # Now call the Leraner  & fit 
      print(country,  P[country])
      L = Learner(args, P[country], df)
      params = L.fit()
      data = [country, "%.6f" % params[0],"%.6f" %params[1], "%.6f" % params[2]]
      df_params.loc[count] = data
      # Let us make prediction with the fitted parameters 
      print(data)
      count +=1

   df_params.to_csv("params_dbsir.csv")

   """  
   E = Epidemology (args.model_name,'solve_ivp',L.data.shape[0]+50)
   E.set_init(L.N, L.I0, L.R0)

   title="Country:" + args.country_name + ", Model:" + args.model_name
   if args.model_name == 'sir':
      sir = E.evolve (params[0], params[1])
      title = title + r', $\beta$' +"=" + str('%.2f' %params[0]) \
         + r', $\gamma$= '+ str('%.2f' % params[1])

   if args.model_name == 'dbsir':
      sir = E.evolve (params[0], params[1], params[2])
      title = title + r', $\beta_0$' +"=" + str('%.2f' %params[0])\
         + r'$\mu$= ' +  str('%.2f' % params[1]) \
         + r', $\gamma$= '+ str('%.2f' % params[2])


   #plt.plot(sir.t,sir.y[0,:],c='b',label='Succeptable')
   plt.plot(sir.t,sir.y[1,:],c='r',label='Infected')
   plt.plot(sir.t,sir.y[2,:],c='g',label='Recovered')
   plt.scatter(L.days, L.data.to_numpy(), c='b',label='Data')
   plt.yscale('log')
   plt.title(title)
   plt.legend()
   plt.savefig("plots/fit_" + args.model_name + ".pdf")
   plt.show()
   """


