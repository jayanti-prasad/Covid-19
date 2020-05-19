import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.optimize import minimize


data_file="../data/covid-19-global.csv"
population_file="../data/world_population.csv"

def get_population(pop_file, country):
   df_p = pd.read_csv(pop_file)
   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()
   return  P[country]

def get_fitting_data (df, country):
   df = df[df['country'] == country]
   df = df.sort_values(by='date')
   data = df['confirmed'] - df['recovered'] - df['deaths']
   data.index = df['date'].to_list()
   data = data [ data > 25]
   return data


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
       self.df_loss = pd.DataFrame(columns=['A','B','t_off','t_w','mse'])
       self.count = 0 

    def fit(self):
       """
       This is the fitting module and you must chose the parameters carefully. 
       """
       return  minimize(self.loss,self.starting_point, method='L-BFGS-B', bounds=self.bounds)

    def loss (self, point):
           
        solution = solve_tbseir (self.t,tbSEIR, self.N,self.I0,self.E0,self.R0,\
           point[0], point[1], point[2], point[3])


        y =  self.data.to_numpy()
        loss_value = np.sqrt(np.mean((solution.y[2] - y)**2))    
        print(point, loss_value)

        return loss_value 


def show_fitting (data, country_name, N, A,B,to,tw):
    I0, R0 = data[0], 0
    E0 = I0
    S0 = N - I0 - R0 - E0

    t = np.arange(0, data.shape[0]+30, 1)
    sol = solve_tbseir (t,tbSEIR,N,I0,E0,R0,A,B,to,tw)


    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot()

    ax.set_title(country_name +", A=" + str("%.4f" %A) + \
      ", B=" + str("%.4f" % B) +\
      r', $t_{off}=$' + str("%.4f" % to)+\
      r', $t_w=$' + str("%.4f" % tw)+\
      r'$, \sigma=\gamma=1/7$')

    
    ax.plot(O.t, data/N,'o',c='b',label='Data')
    ax.plot(sol.t, sol.y[2]/N,c='r',label='Infected')
    ax.legend()
    ax.set_yscale('log')
    plt.show()

if __name__ == "__main__":
  
    country = 'Italy'    

    df = pd.read_csv(data_file)

    N = get_population(population_file, country) 
    data = get_fitting_data (df, country)

    O = Optimizer(N, data,tbSEIR)
    optimal = O.fit()
    params = tuple(optimal.x)
    A, B, to, tw = params

    show_fitting (data, country, N, A,B,to,tw)

    print("A=%.6f," % A, "B=%.6f," % B,"to=%.6f," % to,"tw=%.6f," % tw, "loss=%d," % optimal.fun)
 
