import sys
import os
import argparse 
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from common_utils import get_country_data, strip_year  
from epidemiology import SIR, SEIR, SEIARD, Epidemology 


def get_fitting_data (args, df, country, start_date='2020-01-01'):
   df  = get_country_data (df, country)
   dates = df['date'].to_list()
   data = df['confirmed'] - df['recovered'] - df['deaths']
   data.index = df['date'].to_list()
   return data[start_date:]

def get_population(args, country):
   df_p = pd.read_csv(args.population_file)
   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()
   return  P[country]


def plot_data(data):
   data.index = strip_year(data.index)
   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot(111)
   plt.plot(data)
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   ax.axhline(y=25,c='k',ls='--')
   plt.show()


class Learner(object):
    """
    This is the main optimier class
    """
    def __init__(self, N, data, model):

        self.model = model
        self.data = data 

        I0, R0 = self.data[0], 0  
        S0 =  N - I0 - R0 

        self.E = Epidemology (self.model,'solve_ivp',  data.shape[0])
        self.E.set_init (N, I0, R0)
        print(N, I0, R0, S0)

    def initial_guess (self):

        if self.model == 'sir':
           starting_point =  [0.12, 0.11]
           bounds = [(1.0E-03, 10.0), (1.0E-03, 10.0)]

        if self.model == 'dbsir':
            starting_point = [0.12, 0.01, 0.11]
            bounds = [(1.0E-04, 1.5), (1.0E-4,1.0), (1.0E-04, 1.0)]             

        return starting_point, bounds


    def fit(self):
        """
        This is the fitting module and you must chose the parameters carefully. 

        """
        starting_point, bounds = self.initial_guess() 
        optimal = minimize(self.loss,starting_point, method='L-BFGS-B', bounds=bounds)

        if optimal.success == True:
           return tuple(optimal.x) 
        else:
           print(optimal) 
           return None 

    def loss (self, point):
        if self.model == 'sir':
           solution = self.E.evolve(point[0], point[1])
        if self.model == 'dbsir':
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
   parser.add_argument('-m','--model-name',help='Model',default='dbsir')

   args = parser.parse_args()
   df = pd.read_csv(args.input_file)

   data = get_fitting_data (args, df, args.country_name,'2020-03-04')
   days = [int(i) for i in range(0, data.shape[0])]

   N = get_population(args, args.country_name)

   for index, value in data.items():
       print(f"{index}, {value}")

   # Now call the Leraner  & fit 
   L = Learner(N, data, args.model_name)
   L.initial_guess()
   params = L.fit()
   # Let us make prediction with the fitted parameters 
   print("best fit params:",params)

   E = Epidemology (args.model_name,'solve_ivp',L.data.shape[0]+50)
   E.set_init(N, data[0], 0)

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
   plt.scatter(days, data.to_numpy(), c='b',label='Data')
   #plt.yscale('log')
   plt.title(title)
   plt.legend()
   plt.savefig("plots/fit_" + args.model_name + args.country_name +".pdf")
   plt.show()



