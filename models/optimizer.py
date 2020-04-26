import sys
import os
import argparse 
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from common_utils import get_country_data  
from epidemiology import SIR, SEIR, SEIARD, Epidemology 


class Learner(object):
    """
    This is the main optimier class
    """
    def __init__(self,args, N, df):

        self.args = args
        self.N = N 

        df  = get_country_data (df, args.country_name)
        df = df[df['confirmed'] > 25]
 
        dates = df['date'].to_list() 
        self.data = df['confirmed'] - df['recovered'] - df['deaths']
        self.data.index = dates  
        self.days = [int(i) for i in range(0, len(dates))]

        self.I0, self.R0 = self.data[0], 0  
        self.S0 =  self.N - self.I0 - self.R0 

        self.E = Epidemology (args.model_name,'solve_ivp',  df.shape[0])
        self.E.set_init (self.N, self.I0, self.R0)


    def initial_guess (self):

        if self.args.model_name == 'sir':
           starting_point =  [0.12, 0.11]
           bounds = [(1.0E-03, 10.0), (1.0E-03, 10.0)]

        if self.args.model_name == 'dbsir':
            starting_point = [0.12, 0.01, 0.11]
            bounds = [(1.0E-08, 10.0), (1.0E-4,1.0), (1.0E-08, 10.0)]             

        return starting_point, bounds


    def fit(self):
        """
        This is the fitting module and you must chose the parameters carefully. 

        """
        starting_point, bounds = self.initial_guess() 
        optimal = minimize(self.loss,starting_point, method='L-BFGS-B', bounds=bounds)

        return tuple(optimal.x) 

    def loss (self, point):
        #solution = self.E.evolve(point[0], point[1], point[2])
        if self.args.model_name == 'sir':
           solution = self.E.evolve(point[0], point[1])
        if self.args.model_name == 'dbsir':
           solution = self.E.evolve(point[0], point[1], point[2])

        y =  self.data.to_numpy()
        return np.sqrt(np.mean((solution.y[1] - y)**2))



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

     



   # Now call the Leraner  & fit 
   L = Learner(args, P[args.country_name], df)
   params = L.fit()
   # Let us make prediction with the fitted parameters 
   print("best fit params:",params)
  
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
   plt.savefig("plots/fit_" + args.model_name + args.country_name +".pdf")
   plt.show()



