import os

import numpy as np
import matplotlib.pyplot as plt 
from epidemiology import Epidemology  
import argparse 


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model-name',help='Model Name')
    
    args = parser.parse_args()

    if args.model_name == 'sir':

       # SIR Model 
       N, size, I0, R0, beta, gamma = 1000, 160, 10, 0, 0.24, 0.11
       E = Epidemology ('sir','solve_ivp', size)
       E.set_init(N, I0, R0)
       params = beta, gamma  
       sol = E.evolve (params)
   
       plt.plot(sol.t, sol.y[0],label='Succeptable')
       plt.fill_between(sol.t,0, sol.y[0],color="g", alpha=0.3)
       plt.plot(sol.t, sol.y[1],label='Infection')
       plt.fill_between(sol.t,0, sol.y[1],color="r", alpha=0.3)
       plt.plot(sol.t, sol.y[2],label='Recovered')
       plt.fill_between(sol.t,0, sol.y[2],color="b", alpha=0.3)

    if args.model_name == 'dbsir':

       # decaying beta SIR Model 
       N, size, I0, R0, beta0, mu, gamma = 1000, 160, 10, 0, 0.24, 0.01, 0.11
       E = Epidemology (args.model_name,'solve_ivp', size)
       E.set_init(N, I0, R0)
       params = beta0, mu, gamma,'exp'
       sol = E.evolve (params)

       plt.plot(sol.t, sol.y[0],label='Succeptable')
       plt.fill_between(sol.t,0, sol.y[0],color="g", alpha=0.3)
       plt.plot(sol.t, sol.y[1],label='Infection')
       plt.fill_between(sol.t,0, sol.y[1],color="r", alpha=0.3)
       plt.plot(sol.t, sol.y[2],label='Recovered')
       plt.fill_between(sol.t,0, sol.y[2],color="b", alpha=0.3)

    if args.model_name == 'seir':

       # decaying beta SIR Model 
       N, size, E0, I0, R0, beta, gamma, sigma   \
        = 1000, 160, 10,10, 0, 0.28, 0.05, 0.1
 
       E = Epidemology (args.model_name,'solve_ivp', size)
       E.set_init(N, E0, I0, R0)
       params = beta, gamma, sigma 
       sol = E.evolve (params)

       plt.plot(sol.t, sol.y[0],'g',label='Succeptable')
       plt.fill_between(sol.t,0, sol.y[0],color="g", alpha=0.3)

       plt.plot(sol.t, sol.y[1],'y',label='Exposed')
       plt.fill_between(sol.t,0, sol.y[1],color="y", alpha=0.3)
       
       plt.plot(sol.t, sol.y[2],'r',label='Infection')
       plt.fill_between(sol.t,0, sol.y[2],color="r", alpha=0.3)

       plt.plot(sol.t, sol.y[3],'b',label='Recovered')
       plt.fill_between(sol.t,0, sol.y[2],color="b", alpha=0.3)

    plt.legend()
    #plt.show()
    plt.savefig("plots" + os.sep + args.model_name + ".pdf")

