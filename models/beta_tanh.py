import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import argparse 
from driver_optimizer import get_fitting_data 
from common_utils import get_population,get_top_countries
import pandas as pd
import matplotlib

"""
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)
"""


def SEIR (t, y, N, beta, gamma, sigma):
   S, E, I, R  = y[0]/N, y[1], y[2], y[3]
   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]

def solve_seir (t,model,N,I0,E0,R0,beta,sigma,gamma):
    S0 = N - (I0+E0+R0)
    Y0 = [S0, E0,  I0, R0]
    params = N, beta, sigma, gamma
    solution = solve_ivp(model, [0, t.shape[0]], Y0, t_eval = t,vectorized=True, args=params)
    return solution


#def dbSEIR (t, y, N, beta, gamma, sigma):
#   S, E, I, R  = y[0]/N, y[1], y[2], y[3]
#   beta = beta_t(t, -0.52, 0.80, 18.90, 10.35)
#   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


def beta_t (t, A, B, t_off, t_w):
    #A, B = -0.52, 0.70
    #t_off, t_w = 18.90, 10.35
    y = A * np.tanh ((t-t_off)/t_w) + B
    return y

def tbSEIR (t, y, N, A, B, to, tw):
   S, E, I, R  = y[0]/N, y[1], y[2], y[3]
   sigma = 1.0/7.0
   gamma = 1.0/7.0
   beta = beta_t(t, A, B, to, tw)
   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


def solve_tbseir (t,model,N,I0,E0,R0,A,B,to,tw):
    S0 = N - (I0+E0+R0)
    Y0 = [S0, E0,  I0, R0]
    params = N, A, B, to, tw 
    solution = solve_ivp(tbSEIR, [0, t.shape[0]], Y0, t_eval = t,vectorized=True, args=params)
    return solution


class Optimizer:
    def __init__(self, N, data, model):
       self.model = model
       self.data = data
       self.N = N 
       self.I0, self.R0 = self.data[0], 0
       self.E0 = self.I0 
       self.S0 =  self.N - self.I0 - self.R0 - self.E0 

       self.t = np.arange(0, data.shape[0], 1)

       self.starting_point =  [-0.5, 0.7, 18, 10]
       self.bounds = [(-2.0, 2.0), (1.0E-03, 10.0), (1,30), (1, 30)]

    def fit(self):
       """
       This is the fitting module and you must chose the parameters carefully. 
       """
       optimal = minimize(self.loss,self.starting_point, method='L-BFGS-B', bounds=self.bounds)

       #print("Success:", optimal.success)

       return tuple(optimal.x)


    def loss (self, point):
           
        solution = solve_tbseir (self.t,tbSEIR, self.N,self.I0,self.E0,self.R0,\
           point[0], point[1], point[2], point[3])


        y =  self.data.to_numpy()
        return np.sqrt(np.mean((solution.y[2] - y)**2))


def tester():
    N, I0, E0, R0 = 1000, 10, 1, 0
    beta, sigma, gamma =  0.625, 0.1425, 0.1425
    t = np.arange(1,160,1)

    sol = solve_seir (t,SEIR,N,I0,E0,R0,beta,sigma,gamma) 
    sol1 = solve_seir (t,dbSEIR,N,I0,E0,R0,beta,sigma,gamma) 
   
    plt.plot(sol.t, sol.y[0],c='g', label='Succeptable')
    plt.plot(sol.t, sol.y[1],c='r', label='Exposed')
    plt.plot(sol.t, sol.y[2],c='y', label='Infected')
    plt.plot(sol.t, sol.y[3],c='b', label='Recovered')

    plt.plot(sol1.t, sol1.y[0],':',c='g')
    plt.plot(sol1.t, sol1.y[1],':',c='r',)
    plt.plot(sol1.t, sol1.y[2],':',c='y')
    plt.plot(sol1.t, sol1.y[3],':',c='b')

    plt.legend()
    plt.show()


def show_fitting (data, N, A,B,to,tw):
    I0, R0 = data[0], 0
    E0 = I0
    S0 = N - I0 - R0 - E0

    t = np.arange(0, data.shape[0]+30, 1)
    sol = solve_tbseir (t,tbSEIR,N,I0,E0,R0,A,B,to,tw)

    y_true = data.to_numpy()
    y_pred = sol.y[2,:][:y_true.shape[0]]
    mse  = np.sqrt(np.mean((y_true - y_pred)**2))


    """
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot()

    ax.set_title(args.country_name +", A=" + str("%.4f" %A) + \
      ", B=" + str("%.4f" % B) +\
      r', $t_{off}=$' + str("%.4f" % to)+\
      r', $t_w=$' + str("%.4f" % tw)+\
      r'$, \sigma=\gamma=1/7$')

    
    ax.plot(O.t, data/N,'o',c='b',label='Data')
    #plt.plot(sol.t, sol.y[1]/N,c='r',label='Exposed')
    ax.plot(sol.t, sol.y[2]/N,c='r',label='Infected')
    #plt.plot(sol.t, sol.y[3],c='g',label='Recovered')
    ax.legend()
    ax.set_yscale('log')
    plt.show()
    #plt.savefig("Italy.pdf")
    """
    return mse 

if __name__ == "__main__":
  
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input CSV file')

    args = parser.parse_args()
    df = pd.read_csv(args.input_file)

    countries = get_top_countries(df, 100)
 
    df_out = pd.DataFrame(columns=['country','A','B','t_off','t_w','mse','population'])
    
    count = 0
    for country in countries:
       try:
          N = get_population(country) 
          data = get_fitting_data (args, df, country)

          O = Optimizer(N, data,tbSEIR)
          params = O.fit()
          A, B, to, tw = params
          mse = show_fitting (data, N, A,B,to,tw)
          row = [country, "%.6f" % A, "%.6f" % B,"%.6f" % to,"%.6f" % tw, "%d" % mse, "%d" % N]
          print(row)
          df_out.loc[count] = row
          count +=1   
          #print(A, B, to, tw)
          #show_fitting (data, N, A,B,to,tw)
       except:
          pass 

    df_out.to_csv("results/params_beta_tanh.csv")
       
