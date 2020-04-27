import sys
import os
import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common_utils import get_country_data, date_normalize,country_normalize 
from epidemiology import Epidemology 
from optimizer import Learner 


def get_init_cond (args, df):

   df  = get_country_data (df, args.country_name)
   df_p = pd.read_csv(args.population_file)

   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()
   N = P[args.country_name]

   df = df[df['confirmed'] > 50]
   dates = df['date'].to_list()
   data = df['confirmed'] - df['recovered'] - df['deaths']
   data.index = dates
   I0, R0 = data[0], 0

   return N, I0, R0, data 




if __name__ == "__main__":
   """
   The main program 
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country Name')
   parser.add_argument('-p','--population-file',help='Country population file',default='../data/world_population.csv')
   parser.add_argument('-m','--model-name',help='Model',default='sir')
   parser.add_argument('-n','--num-days',help='Number of days',default=100,type=int)

   args = parser.parse_args()

   df = pd.read_csv(args.input_file)
   df_params = pd.read_csv("params.csv")

   X = df_params.loc[df_params['country'] == args.country_name]

   #P = str(X.values).split() 
   params = X.values[0][2],X.values[0][3],X.values[0][4]
   #print(X.values[0][2])
   #print(params)
   #sys.exit()


   #X.index = [0 for i in range(0, X.shape[0])]
   #beta_0, mu, gamma = X['beta'][0], X['mu'][0], X['gamma'][0]
   #params = beta_0, mu, gamma 

   N, I0, R0, data = get_init_cond (args, df)
   x  = [int(i) for i in range(0, data.shape[0])]

   L = Learner(args, N, df, args.country_name)
   #params = beta_0, mu, gamma 
   params = L.fit()
   print("params:",params)
   #print("params1:",params1)
   #sys.exit()

   
   #print("beta_0, mu, gamma=",beta_0, mu, gamma)
   #print("N, I0, R0=", N, I0, R0)

   #E = Epidemology (args.model_name,'solve_ivp', args.num_days)
   #E.set_init(N, I0, R0)

   title="Country:" + args.country_name + ", Model:" + args.model_name

   sir = E.evolve (params[0], params[1], params[2])
   title = title + r', $\beta_0$' +"=" + str('%.2f' %params[0])\
      + r'$\mu$= ' +  str('%.2f' % params[1]) \
      + r', $\gamma$= '+ str('%.2f' % params[2])

   #plt.plot(sir.t,sir.y[0,:],c='b',label='Succeptable')
   plt.plot(sir.t,sir.y[1,:],c='r',label='Infected')
   plt.plot(sir.t,sir.y[2,:],c='g',label='Recovered')
   plt.scatter(x, data.to_numpy(), c='b',label='Data')
   plt.yscale('log')
   plt.title(title)
   plt.legend()
   plt.savefig("plots/fit_" + args.country_name + ".pdf")
   plt.show()


