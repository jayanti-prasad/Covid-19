import sys
import os
import argparse 
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from common_utils import date_normalize 


def get_population(args):
    """
    Get the population of the country 
    """
    df_l = pd.read_csv(args.lockdown_file)
    # Read the population and the lockdown date 
    population = dict(zip(df_l['country'].to_list(), df_l['population'].to_list()))
    return  population[args.country_name]


def get_country_data (df, country, start_date):
    """
    Get country data. Note that I'(t) =  I(t) - R(t) - D(t) 
    """
    country_df = df[df['country'] == country]
    data_c = country_df['confirmed']
    data_r = country_df['recovered']
    data_d = country_df['deaths']
    data = data_c - data_r - data_d
    data.index = country_df['date'].to_list()
    return data.loc[start_date:]

    
def SEIR (t, y, N, beta, sigma, gamma):
   """
   This is SEIR Model can be used for SIR also with setting
   sigma = 0  and adding 'I' and 'E'
   """ 
   S, E, I, R  = y[0], y[1], y[2], y[3]
   return [-beta*S*I/N, beta*S*I/N-sigma*E, sigma*E-gamma*I, gamma*I]


def solve_ode (beta, sigma, gamma,  size, N, E0, I0, R0):
   """
   ODE Solver, can be used for just solving SEIR equations also. 
   """
   S0 = N - I0 - R0 - E0 
   solution = solve_ivp(SEIR, [0, size], [S0,E0, I0,R0],\
     t_eval = np.arange(0, size, 1), vectorized=True, args=(N,beta,sigma,gamma))
   return solution


def loss(point, data, N, E0, I0, R0):
    """
    Mean square error. Note that we are fitting only I(t)
    """
    size = len(data)
    beta, sigma, gamma = point
    S0 = N - I0 - R0 - E0 
    solution = solve_ode (beta, sigma, gamma, size, N, E0, I0, R0) 

    return np.sqrt(np.mean((solution.y[1] - data)**2))


class Learner(object):
    """
    This is the main optimier class
    """
    def __init__(self, args, df, loss, N, E0, I0, R0):
        self.N = N 
        self.E0 = E0 
        self.I0 = I0
        self.R0 = R0 
        self.S0 = self.N - I0 - E0 - R0 
        self.loss = loss
        self.data = get_country_data (df, args.country_name, args.start_date)


    def extend_index(self, index, new_size):
       """
       Using the parameter learned we can compute S,E,I and R future dates also. 
       """
       values = index.values
       current = datetime.strptime(index[-1], '%Y-%m-%d')
       while len(values) < new_size:
          current = current + timedelta(days=1)
          values = np.append(values, datetime.strftime(current, '%Y-%m-%d'))
       return values


    def predict(self, beta, sigma, gamma, data, predict_range):
        """
        Prediction Method
        """
        new_index = self.extend_index(data.index, predict_range)
        size = len(new_index)
        extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))
        solution = solve_ode (beta, sigma, gamma, size, self.N, self.E0, self.I0, self.R0) 
        return new_index, extended_actual, solution 


    def fit(self):
        """
        This is the fitting module and you must chose the parameters carefully. 

        """
        optimal = minimize(
            loss,
            [0.001, 0.001, 0.001], # Starting values 
            args=(self.data, self.N, self.E0, self.I0, self.R0),
            method='L-BFGS-B',
            bounds=[(1.0E-08, 1.0), (1.0E-08, 1.0), (1.0E-8,1.0)]
        )
        beta, sigma, gamma = optimal.x
        return beta, sigma, gamma  


if __name__ == "__main__":
   """
   The main program 
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country Name')
   parser.add_argument('-l','--lockdown-file',help='Country details file',default='../data/covid-19-lockdown.csv')
   parser.add_argument('-d','--start-date',help='Starting date',default='2020-02-01')
   parser.add_argument('-n','--num-days',help='Number of days',type=int,default=160)
   parser.add_argument('-s','--sigma',help='sigma',type=float,default=0.1)
   parser.add_argument('-b','--beta',help='Beta',type=float,default=0.21)
   parser.add_argument('-g','--gamma',help='Gamma',type=float,default=0.1)

   args = parser.parse_args()
   print(args)


   start_date = args.start_date

   # Read the data, normalize dates and sort the rows by dates 
   # and finally get the data for a given country 
   df = pd.read_csv(args.input_file)
   df = date_normalize (df)
   df = df.sort_values(by='date')
   data = get_country_data (df, args.country_name, args.start_date)

   # Get the population of the country 
   N = get_population (args)
   print("Country:",args.country_name,"Population:",N)

   xx = [i for i in range(0, len(data))]
   print("I0=",data[start_date])

   # We do not know starting exposed population so we must guess 
   # something. 
   ei = float(data[start_date]) 
   alpha = 0.0 
   E0, I0, R0  = alpha * ei, (1-alpha) * ei,  0  

   # Now call the Leraner  & fit 
   L = Learner(args, df, loss, N, E0, I0, R0)
   beta, sigma, gamma = L.fit()

   # Print the parameters 
   print("beta=",beta,"sigma=",sigma, "gamma=",gamma,"I0=",I0,"data size=", len(data))

   # Get the prediction for a given number of days 
   new_indx, predict, sir  = L.predict(beta,sigma,gamma,data,args.num_days)
   #sir  = solve_ode (args.beta, args.sigma, args.gamma, args.num_days, N,E0, I0, R0)
   #sir  = solve_ode (beta, sigma, gamma, args.num_days, N,I0,0,R0)

   #plt.plot(sir.t,sir.y[0,:],c='g',label='Succeptable')
   plt.plot(sir.t,np.log(sir.y[1,:]),c='k',label='Exposed')
   plt.plot(sir.t,np.log(sir.y[2,:]),c='r',label='Infected')
   plt.plot(sir.t,np.log(sir.y[3,:]),c='b',label='Recovered')
   plt.scatter(xx, np.log(data.values),c='y',label='Data')

   plt.legend()
   plt.show()



