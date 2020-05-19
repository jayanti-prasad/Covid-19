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


def get_country_data (df, country, start_date):
    country_df = df[df['country'] == country]
    data_c = country_df['confirmed']
    data_r = country_df['recovered']
    data_d = country_df['deaths']
    data = data_c - data_r - data_d
    data.index = country_df['date'].to_list()
    return data.loc[start_date:]

    
def SIR (t, y, N, beta, gamma):
   S, I, R  = y[0]/N, y[1], y[2]
   return [-beta*S*I, beta*S*I-gamma*I, gamma*I]

def SEIR (t, y, N, beta, gamma, sigma):
   S, E, I, R  = y[0]/N, y[1], y[2], y[3]
   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


def solve_ode (beta, gamma, size, N, I0, R0):
   S0 = N - I0 - R0
   solution = solve_ivp(SIR, [0, size], [S0,I0,R0],\
     t_eval=np.arange(0, size, 1), vectorized=True, args=(N,beta,gamma))
   return solution 


def solve_ode1 (beta, gamma, sigma,  size, N, E0, I0, R0):
   S0 = N - I0 - R0 - E0 
   solution = solve_ivp(SEIR, [0, size], [S0,E0, I0,R0],\
     t_eval=np.arange(0, size, 1), vectorized=True, args=(N,beta,gamma,sigma))
   return solution


def loss(point, data, N, I0, R0):
    size = len(data)
    beta, gamma = point
    S0 = N - I0 - R0
    solution = solve_ode (beta, gamma, size, N,I0, R0) 

    return np.sqrt(np.mean((solution.y[1] - data)**2))


def loss_double(point, data, N, I0, R0):
    size = len(data)
    beta, gamma = point
    S0 = N - I0 - R0
    solution = solve_ode (beta, gamma, size, N, I0, R0) 
    l1 = np.sqrt(np.mean((solution.y[1] - data)**2))
    l2 = np.sqrt(np.mean((solution.y[2] - recovered)**2))
    alpha = 0.1
    return alpha * l1 + (1 - alpha) * l2


class Learner(object):
    def __init__(self, args, df, loss, N, I0, R0):
        self.N = N 
        self.I0 = I0
        self.R0 = R0 
        self.S0 = self.N - self.I0 - self.R0 
        self.loss = loss
        self.data = get_country_data (df, args.country_name, args.start_date)


    def extend_index(self, index, new_size):
       values = index.values
       current = datetime.strptime(index[-1], '%Y-%m-%d')
       while len(values) < new_size:
          current = current + timedelta(days=1)
          values = np.append(values, datetime.strftime(current, '%Y-%m-%d'))
       return values


    def predict(self, beta, gamma, data, predict_range):
        new_index = self.extend_index(data.index, predict_range)
        size = len(new_index)
        extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))
        solution = solve_ode (beta, gamma, size, self.N,self.I0, self.R0) 
        return new_index, extended_actual, solution 


    def fit(self):
        optimal = minimize(
            loss,
            [0.001, 0.001],
            args=(self.data, self.N, self.I0, self.R0),
            method='L-BFGS-B',
            bounds=[(1.0E-06, 1.0), (1.0E-06, 1.0)]
        )
        beta, gamma = optimal.x
        return beta, gamma  


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country Name',default='Italy')
   parser.add_argument('-s','--start-date',help='Starting date',default='2020-03-01')
   parser.add_argument('-n','--num-days',help='Number of days',type=int,default=160)
   parser.add_argument('-b','--beta',help='Beta',type=float,default=0.21)
   parser.add_argument('-g','--gamma',help='Gamma',type=float,default=0.1)

   args = parser.parse_args()

   start_date = args.start_date
   print("starting date:", start_date)

   df = pd.read_csv(args.input_file)
   df = date_normalize (df)
   df = df.sort_values(by='date')
   
   data = get_country_data (df, args.country_name, args.start_date)
   xx = [i for i in range(0, len(data))]
   print("I0=",data[start_date])

   N, I0, R0  = 6.0E8, float(data[start_date]), 0  

   L = Learner(args, df, loss, N, I0, R0)
   beta, gamma = L.fit()

   print("beta=",beta,"gamma=",gamma,"I0=",I0,"data size=", len(data))

   new_indx, predict, sir  = L.predict(beta,gamma,data,args.num_days)
   #sir  = solve_ode (args.beta, args.gamma, args.num_days, N,I0, R0)
   sir  = solve_ode1 (args.beta, args.gamma,0.011,args.num_days, N,I0,0,R0)


   plt.plot(sir.t,sir.y[0,:],c='g',label='Succeptable')
   plt.plot(sir.t,sir.y[1,:],c='r',label='Infected')
   plt.plot(sir.t,sir.y[2,:],c='b',label='Recovered')
   plt.scatter(xx, data.values,c='y',label='Data')

   plt.legend()
   plt.show()



