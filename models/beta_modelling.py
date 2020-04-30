import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt 
import sys
from epidemiology import dbSIR 
import matplotlib

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 12}

matplotlib.rc('font', **font)


def beta_t (t, b0, mu):
  return  b0* np.exp(- mu * t)


def SIR (t, y, N, b0, mu, gamma):
   beta = beta_t (t, b0, mu)
   S, I, R  = y[0]/N, y[1], y[2]
   return [-beta*S*I, beta*S*I-gamma*I, gamma*I]


if __name__ == "__main__":

    N, I0, R0 = 1000, 10, 0
    S0 = N - I0 - R0
    Y0 = [S0, I0, R0]
    size = 160 
    t = np.arange(1, size, 1)

    params1 = N, 0.24, 0.00, 0.10
    params2 = N, 0.24, 0.01, 0.10

    y = [ beta_t (x, 0.24, 0.01) for x in t]
    
    sol1= solve_ivp(dbSIR, [1, size], Y0,\
            t_eval = t,vectorized=True, args=params1)

    sol2= solve_ivp(dbSIR, [1, size], Y0,\
            t_eval = t,vectorized=True, args=params2)

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    #bx = fig.add_subplot(122)


    ax.plot(sol1.t, sol1.y[0],'g', label='Succeptable')
    ax.plot(sol1.t, sol1.y[1],'r', label='Infected')
    ax.plot(sol1.t, sol1.y[2],'b', label='Removed')

    ax.plot(sol2.t, sol2.y[0],'g:')
    ax.plot(sol2.t, sol2.y[1],'r:')
    ax.plot(sol2.t, sol2.y[2],'b:')
    ax.set_title("Solid for fixed " + r'$\beta$' +" and dotted for decaying "+ r'$\beta$')
    ax.set_xlabel('time')

    ax.legend()
    #ax.legend(loc='upper center', bbox_to_anchor=(0.25, 1.0),
    #      ncol=3, fancybox=True, shadow=True)


    #bx.plot(t, y)
    #bx.set_xlabel('time')
    #bx.set_ylabel(r'$\beta(t)$')
    #bx.set_title("Time varying beta " + r'$\beta (t) = \beta_0 e^{-\mu t}$')
    plt.savefig("results_R0/dbsir.pdf")


    plt.show()