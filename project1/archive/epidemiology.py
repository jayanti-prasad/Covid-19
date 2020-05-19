import numpy as np
from scipy.integrate import solve_ivp

"""
The main module to solve the dynamical equations of Epidemiology
"""

def SIR (t, y, *args):
   """
   Succeptable-Infected-Recovered model.
   Input :
      y : S0, I0, R0  (initial condition)
      N : Population size
      beta, gamma : Usual parameters
   """

   N, beta, gamma = args[0], args[1], args[2]
   S, I, R  = y[0]/N, y[1], y[2]

   return [-beta*S*I, beta*S*I-gamma*I, gamma*I]


def dbSIR (t, y, *args):

   N, b0, mu, gamma = args[0], args[1], args[2], args[3]

   #if args[4] == 'exp':
   beta_t = lambda t: b0 * np.exp (-mu *t)
   #if args[4] == 'tanh':
   #   beta_t = lambda t: b0 * (1 -  np.tanh(mu*t))

   beta = beta_t (t)
   S, I, R  = y[0]/N, y[1], y[2]
   return [-beta*S*I, beta*S*I-gamma*I, gamma*I]


def SEIR (t, y, *args):
   """
   Succeptable-Exposed-Infected-Recovered model.
   One extra parameter sigma and 
   One extra initial condition for exposed - E0
   """
   N, beta, gamma, sigma =\
      args[0], args[1], args[2], args[3]

   S, E, I, R  = y[0]/N, y[1], y[2], y[3]

   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


def SEIARD (t, y,  N, beta, sigma, gamma, delta, p):
   """
   Reference : https://arxiv.org/pdf/2004.08288.pdf
   Deafult parameters :

   N, beta, sigma, gamma, delta, p =\
   1000, 0.46, 0.14, 0.01, 0.01, 0.8

   E0, I0, A0, RI0, RA0, D0 =\
   10, 10, 0, 0, 0, 0

   t = np.arange(0, 160, 1)

   """
   S, E, I, A, RI, RA, D =\
     y[0], y[1], y[2], y[3], y[4], y[5], y[6]

   f = (I-A) / (N-D)
 
   dSdt = -beta * S * f
   dEdt =  beta * S * f  - sigma * E
   dIdt = p * sigma * E - (delta + gamma ) * I
   dAdt = (1.0 -p ) * sigma * E - gamma * A
   dRidt = gamma * I
   dRadt = gamma * A
   dDdt  = delta * I

   return  [dSdt, dEdt, dIdt, dAdt, dRidt, dRadt,  dDdt]


class Epidemology:
    def __init__(self, *args):
       self.model  = args[0]
       self.solver = args[1]
       self.size   = args[2]
       self.t = np.arange(0, self.size, 1)
   
    def set_init (self, *args):
       if self.model == 'sir':
          [self.N, self.I0, self.R0] = args[0], args[1], args[2] 

       if  self.model == 'dbsir':
          [self.N, self.I0, self.R0] = args[0], args[1], args[2]


       if self.model == 'seir':
          [self.N, self.E0, self.I0, self.R0] = args[0], args[1], args[2], args[3]
 
       if self.model == 'seiard':
          [self.N, self.E0, self.I0, self.A0, self.RI0, self.RA0, self.D0] =\
             args[0], args[1], args[2], args[3],args[4], args[5], args[6]
 

    def evolve (self, args):
        """
        This is the main evolution mthod.
        > evolve (beta, gamma) : for SIR 
        > evolve (beta, sigma, gamma) : for SEIR 
        """
        
        if self.model == 'sir':
           self.S0 = self.N - self.I0 - self.R0 
           Y0 = [self.S0, self.I0, self.R0]   
           params = self.N, args[0], args[1]      
           #params = N, beta, gamma      
           func = SIR 
 
        if self.model == 'dbsir':
           self.S0 = self.N - self.I0 - self.R0 
           Y0 = [self.S0, self.I0, self.R0]   
           params = self.N, args[0], args[1], args[2] 
           #params = N, beta_0, mu, sigma, gamm  
           func = dbSIR 


        if self.model == 'seir':
           self.S0 = self.N - self.E0 - self.I0 -  self.R0 
           Y0 = [self.S0, self.E0, self.I0, self.R0]   
           #params = N, beta, gamma, sigma 
           params = self.N, args[0], args[1], args[2]      
           func = SEIR 

        if self.model == 'seiard':
           beta, sigma, gamma, delta, p = args[0], args[1],\
               args[2], args[3], args[4] 
  
           self.S0 = self.N - (self.E0 + self.I0 + self.A0 +\
              self.RI0 + self.RA0 + self.D0)

           Y0 = [self.S0, self.E0, self.I0, self.A0, self.RI0,\
              self.RA0, self.D0]
           params = self.N,  beta, sigma, gamma, delta, p
           func = SEIARD


        solution = solve_ivp(func, [0, self.size], Y0,\
            t_eval = self.t,vectorized=True, args=params)

        return solution
