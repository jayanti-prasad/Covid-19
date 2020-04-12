import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import argparse
import pandas as pd


# The SIR model differential equations.
def deriv(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * E
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt


def solve_seir (S0,E0,I0,R0,args):
    # Initial number of infected and recovered individuals, I0 and R0.
    N = args.num_pop 
    t = np.linspace(0,300, 300)
    y0 = S0, E0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, args.beta, args.sigma, args.gamma))
    S, E, I, R = ret.T
    return t, S, E, I, R 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--num-pop',type=int,default=1300000000,help='Population size')
    parser.add_argument('-d','--num-days',type=int,default=160,help='Number of days')
    parser.add_argument('-b','--beta',type=float,default=0.625,help='Parameter beta ')
    parser.add_argument('-g','--gamma',type=float,default=0.1,help='Parameter gamma')
    parser.add_argument('-s','--sigma',type=float,default=0.14285,help='Parameter sigma')

    args = parser.parse_args()

    m, N = args.num_days, args.num_pop
    df = pd.read_csv("../data/India.csv")

    yy = df['confirmed'].to_numpy()
    xx = np.array([int(i) for i in range(0, len(yy))])

   
    N = args.num_pop
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, R0, E0 = 28, 0, 30
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0

    t, S, E, I, R = solve_seir (S0,E0,I0,R0,args)

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111)

    ax.plot(t, S/N, 'b',label='Susceptible')
    ax.plot(t, E/N, 'k',label='Exposed')
    ax.plot(t, I/N, 'r',label='Infected')
    ax.plot(t, R/N, 'g',label='Recovered with immunity')

    ax.set_xlabel('Time /days')
    ax.set_ylabel('Number (1000s)')
    ax.set_ylim(0,1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
       ax.spines[spine].set_visible(False)
    plt.show()
