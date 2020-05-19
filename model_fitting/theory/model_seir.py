import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import sys

def get_beta (beta0,t0,tw,t):
   rho  = 0.75
   beta = lambda t : 1.0 - rho * (t-t0)/t

   if t > t0 and t < t0+tw  :
      beta_t = beta0
   else :
      beta_t = beta0 * beta (t)

   return beta_t

# The SIR model differential equations.
def deriv_t(y, t, N, beta, sigma, gamma):

    beta_t = get_beta (beta,40,21,t) 
    
    S, E, I, R = y
    dSdt = -beta_t * S * I / N
    dEdt = beta_t * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


# The SIR model differential equations.
def deriv(y, t, N, beta, sigma, gamma):

    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


def solve_seir (S0,E0,I0,R0,args,flag=0):
    # Initial number of infected and recovered individuals, I0 and R0.
    N = args.num_pop 

    t = np.linspace(1,args.num_days, args.num_days)
    print("t==",t )

    y0 = S0, E0, I0, R0

    if flag == 1:
       ret = odeint(deriv_t, y0, t, args=(N, args.beta, args.sigma, args.gamma))
    else:
       ret = odeint(deriv, y0, t, args=(N, args.beta, args.sigma, args.gamma))

    S, E, I, R = ret.T

    return t, S, E, I, R 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--num-pop',type=int,default=1300000000,help='Population size')
    parser.add_argument('-d','--num-days',type=int,default=160,help='Number of days')
    parser.add_argument('-b','--beta',type=float,default=0.625,help='Parameter beta ')
    parser.add_argument('-g','--gamma',type=float,default=0.14285,help='Parameter gamma')
    parser.add_argument('-s','--sigma',type=float,default=0.14285,help='Parameter sigma')

    args = parser.parse_args()

    m, N = args.num_days, args.num_pop
    df = pd.read_csv("../data/covid-19-India.csv")

    yy = df['confirmed'].to_numpy()
    xx = np.array([int(i) for i in range(0, len(yy))])

   
    N = args.num_pop
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, R0, E0 = 28, 0, 30
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0 -E0

    t, S, E, I, R = solve_seir (S0,E0,I0,R0,args,0)
    t1, S1, E1, I1, R1 = solve_seir (S0,E0,I0,R0,args,1)

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w',figsize=(12,12))
    ax = fig.add_subplot(211)
    bx = fig.add_subplot(212)

    beta_t = [get_beta (args.beta,41,21,i) for i in t] 

    #bx.plot(t,beta_t)
    print("t=",t)
    print("beta_t=",beta_t)
    sys.exit()

    ax.set_title(r'$\beta=$'+str(args.beta)\
      + r', $\sigma=$'+str(args.sigma)\
      +r', $\gamma=$'+str(args.gamma)+",N="+str(N)\
      +",S0="+str(S0)+",I0="+str(I0)+",E0="+str(E0)+",R0=0")

    ax.plot(t, S/N, 'b',label='Susceptible')
    ax.plot(t, E/N, 'k',label='Exposed')
    ax.plot(t, I/N, 'r',label='Infected')
    ax.plot(t, R/N, 'g',label='Recovered with immunity')

    ax.plot(t, S1/N, 'b:')
    ax.plot(t, E1/N, 'k:')
    ax.plot(t, I1/N, 'r:')
    ax.plot(t, R1/N, 'g:')

    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number (in Ns)')
    ax.set_ylim(0,1.2)
    ax.legend()
    plt.show()
    #plt.savefig("SEIR.pdf")
