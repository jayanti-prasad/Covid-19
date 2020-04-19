import numpy as np
from scipy.integrate import solve_ivp


def SIR (t, y, N, beta, gamma):
   S, I, R  = y[0]/N, y[1], y[2]
   return [-beta*S*I, beta*S*I-gamma*I, gamma*I]


def SEIR (t, y, N, beta, gamma, sigma):
   S, E, I, R  = y[0]/N, y[1], y[2], y[3]
   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


class Epidemology:
    def __init__(self, *args):
       self.model  = args[0]
       self.solver = args[1]
       self.size   = args[2]
       self.t = np.arange(0, self.size, 1)
   
    def set_init (self, *args):
       if self.model == 'sir':
         [self.N, self.I0, self.R0] = args[0], args[1], args[2] 
       
       if self.model == 'seir':
         [self.N, self.E0, self.I0, self.R0] = args[0], args[1], args[2], args[3]
 

    def evolve (self, *args):
        if self.model == 'sir':
           beta,  gamma = args[0], args[1]
           self.S0 = self.N - self.I0 - self.R0 
           Y0 = [self.S0, self.I0, self.R0]   
           params = self.N, beta, gamma      
           func = SIR 

        if self.model == 'seir':
           beta, sigma, gamma = args[0], args[1], args[2] 
           self.S0 = self.N - self.E0 - self.I0 - self.R0 
           Y0 = [self.S0, self.E0,  self.I0, self.R0]   
           params = self.N, beta, sigma, gamma      
           func = SEIR 

        solution = solve_ivp(func, [0, self.size], Y0,\
            t_eval = self.t,vectorized=True, args=params)

        return solution
