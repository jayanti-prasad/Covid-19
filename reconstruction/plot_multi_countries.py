import os
import sys
import pandas as pd
import numpy as np
import argparse
import matplotlib 
import matplotlib.pyplot as plt
from common_utils import lockdown_info, get_country_data, strip_year
from common_utils import get_country_data,strip_year
from matplotlib.ticker import AutoMinorLocator
from beta_solver import  BetaSolver

fontsize = 22 
matplotlib.rc('xtick', labelsize=fontsize) 
matplotlib.rc('ytick', labelsize=fontsize) 
matplotlib.rcParams['axes.linewidth'] = 2.0
matplotlib.rcParams["font.family"] = "Courier New"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
    parser.add_argument('-o','--output-dir',help='Output dir', default='results')
    parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    df = pd.read_csv(args.input_file)

    alpha, sigma_in, gamma_in = 1.0, 7.0, 7.0 

    countries = ['Germany','US','Spain','France','Iran','India']

    fig = plt.figure(figsize=(16,18))

    ax = []
    ax.append(fig.add_subplot(321))
    ax.append(fig.add_subplot(322))
    ax.append(fig.add_subplot(323))
    ax.append(fig.add_subplot(324))
    ax.append(fig.add_subplot(325))
    ax.append(fig.add_subplot(326))

    for a in ax:
      a.set_xlim(-1,67)
      a.set_ylim(-8.0,11.0)

    plt.subplots_adjust(wspace=0, hspace=0)

    count = 0
    for country in countries:

        N, L, T  = lockdown_info (args.lockdown_file, country)

        df1 = get_country_data (df, country)
        df1 = df1[df1['confirmed'] > 25] 
        print(country, df1.shape)

        R = BetaSolver(df1, N)

        beta = R.solve(gamma_in, sigma_in, alpha)

        lockdown = beta.index.get_loc(L, method ='ffill')

        dates = beta.index  
        y = beta 
        days = np.array([i for i in range (0, beta.shape[0])])
 
        print(count+1,'&',country,'&', N,'&', T, '&', dates[0], '&', L,' \\\ \hline') 

        ax[count].set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)

        if count % 2==  0: 
            ax[count].set_ylabel('Raw '+ r'$\beta$(t)',fontsize=fontsize)
         
        if count %2 !=0:
            ax[count].yaxis.tick_right()

        if count == 0 or count == 2: 
            ax[count].tick_params(labelbottom=False) 
 
        xx , yy = days[:-2], y[:-2]

        ax[count].axvline(x=float(lockdown),c='k',ls='--')
        ax[count].axhline(y=0,c='k',ls='--')

        ax[count].plot(xx,yy,lw='2',label=country)
        ax[count].scatter(xx,yy)

        plt.setp(ax[count].get_xticklabels(), rotation=90, horizontalalignment='right')
        ax[count].legend(fontsize=fontsize)
        ax[count].xaxis.set_minor_locator(AutoMinorLocator())
        ax[count].xaxis.grid(True, which='both')
        count +=1

    plt.savefig(args.output_dir + os.sep + "multi_countries.pdf")
    plt.show()
       
