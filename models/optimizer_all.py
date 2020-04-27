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
from optimizer import Learner, get_fitting_data, get_population 


def get_top_countries(df, count):
    df = country_normalize(df)
    df1 = df.copy()
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0]
    df_top = df1[df1['date'] == last_date]
    df_top = df_top.sort_values(by=['confirmed'],ascending=False)[:count]
  
    return df_top['country'].to_list()


def show_fitting(args, N, data, country_name, params):

   E = Epidemology (args.model_name,'solve_ivp',data.shape[0]+50)
   E.set_init(N, data[0], 0)
   days = [int(i) for i in range(0, data.shape[0])]

   sir = E.evolve (params[0], params[1], params[2])
   title = country_name  + r', $\beta_0$' +"=" + str('%.2f' %params[0])\
      + r'$\mu$= ' +  str('%.2f' % params[1]) \
      + r', $\gamma$= '+ str('%.2f' % params[2])

   plt.plot(sir.t,sir.y[1,:],c='r',label='Infected')
   plt.plot(sir.t,sir.y[2,:],c='g',label='Recovered')
   plt.scatter(days, data.to_numpy(), c='b',label='Data')
   plt.yscale('log')
   plt.title(title)
   plt.legend()
   plt.savefig("plots_fit" + os.sep +  country_name + ".pdf")
   plt.show()


if __name__ == "__main__":
   """
   The main program 
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',default='../data/covid-19-global.csv')
   parser.add_argument('-p','--population-file',help='Country population file',default='../data/world_population.csv')
   parser.add_argument('-m','--model-name',help='Model',default='dbsir')

   args = parser.parse_args()
   df = pd.read_csv(args.input_file)

   countries = get_top_countries(df, 50)

   df_params = pd.DataFrame(columns=['country','beta_0','mu','gamma'])
   count = 0
   for country in countries:
      data = get_fitting_data (args, df, country,'2020-03-04')
      days = [int(i) for i in range(0, data.shape[0])]
      N = get_population(args, country)

      L = Learner(N, data, args.model_name)
      L.initial_guess()
      params = L.fit()

      if params:
         data_row = [country, "%.6f" % params[0],"%.6f" %params[1], "%.6f" % params[2]]
         df_params.loc[count] = data_row 
         # Let us make prediction with the fitted parameters 
         print(data_row)
         show_fitting(args, N, data, country, params)
         count +=1

   df_params.to_csv("params.csv")

