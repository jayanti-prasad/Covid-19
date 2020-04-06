import os
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import argparse


"""
This program solve the SIR equation numerically for a given set of
parameters. The parameters which can be given at the command line 
are as follows:

N : Population size 
beta : Parameter represenating the infection rate
gamma : Parameter representing the recovering rate

The outputs are :
S(t) : The number of people remaining succeptable (healthy)
I(t) : The number of people getting infected 
R(t) : The number of people getting recovered 

Jayanti Prasad Ph.D [prasad.jayanti@gmail.com]

"""



def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-n', '--num-people', help='Number of people', type=int, default=1000)
   parser.add_argument('-b', '--beta', help='S decay param', type=float, default=0.2)
   parser.add_argument('-g', '--gamma', help='R growth param', type=float, default=0.1)
   parser.add_argument('-o', '--output-dir', help='Output dir')
   args = parser.parse_args()

   os.makedirs(args.output_dir, exist_ok=True)

   # Total population, N.
   N = args.num_people 
   # Initial number of infected and recovered individuals, I0 and R0.

   I0, R0 = 1, 0
   # Everyone else, S0, is susceptible to infection initially.
   S0 = N - I0 - R0

   # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
   beta, gamma = args.beta, args.gamma   

   # A grid of time points (in days)
   t = np.linspace(0, 160, 160)

   # Initial conditions vector
   y0 = S0, I0, R0
   # Integrate the SIR equations over the time grid, t.
   ret = odeint(deriv, y0, t, args=(N, beta, gamma))
   S, I, R = ret.T

   plt.plot(t, S,'g', label='Susceptible')
   plt.plot(t, I,'r', label='Infected')
   plt.plot(t, R,'b', label='Recovered with immunity')
   plt.legend()
   plt.savefig(args.output_dir + os.sep + "sir_solver_plot.pdf")

