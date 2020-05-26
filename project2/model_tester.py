import os
import numpy as np
import matplotlib.pyplot as plt 
from PyCov19.epidemiology import Epidemology  
from PyCov19.epd_models import SIR, SIRD 
from PyCov19.beta_models import exp, tanh
import argparse 
import matplotlib


font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['axes.linewidth'] = 2.0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-e','--epd-model',help='EPD model')
    parser.add_argument('-b','--beta-model',help='beta model')
    
    args = parser.parse_args()

    N = 1000 
    E = Epidemology ('solve_ivp',eval(args.epd_model),eval(args.beta_model))
 
    if args.epd_model == 'SIR':
       Y0 = 10, 0
       params = [0.1,0.24, 0.0,0.0, 10000]
       # gamma, beta_0, alpha, mu, tl 
       
    if args.epd_model == 'SIRD':
       Y0 = 10, 0, 0 
       params = [0.05,0.01, 0.44, 0.0,0.0, 10000]
       # gamma, delta,  beta_0, alpha, mu, tl 
 
    E.set_init (N=N, Y0=Y0)

    sol = E.evolve (160, params)

    fig = plt.figure(figsize=(12,9))
    ax = fig.add_subplot(111)
   
    ax.plot(sol.t, sol.y[0],label='Succeptable')
    ax.fill_between(sol.t,0, sol.y[0],color="g", alpha=0.3)

    ax.plot(sol.t, sol.y[1],label='Infected')
    ax.fill_between(sol.t,0, sol.y[1],color="r", alpha=0.3)
    ax.plot(sol.t, sol.y[2],label='Recovered')
    ax.fill_between(sol.t,0, sol.y[2],color="b", alpha=0.3)


    if args.epd_model == 'SIR':
       ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=True, shadow=True)

    if args.epd_model == 'SIRD':
       ax.plot(sol.t, sol.y[3],label='Dead')
       ax.fill_between(sol.t,0, sol.y[3],color="y", alpha=0.3)
       ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=4, fancybox=True, shadow=True)
    
    #plt.legend()
    plt.show()
    #plt.savefig("plots" + os.sep + args.epd_model + ".pdf")


