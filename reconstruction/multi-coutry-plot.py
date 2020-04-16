import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob 
import matplotlib 
import numpy as np
from common_utils import get_country_data,strip_year
import arrow
from matplotlib.ticker import AutoMinorLocator
from reconstruction import Reconstruct
import argparse

fontsize = 22 
matplotlib.rc('xtick', labelsize=fontsize) 
matplotlib.rc('ytick', labelsize=fontsize) 
matplotlib.rcParams['axes.linewidth'] = 2.0
matplotlib.rcParams["font.family"] = "Courier New"
matplotlib.rcParams['axes.labelweight'] = 'bold'


def read_lockdown (args):
    df_l = pd.read_csv('../data/covid-19-lockdown.csv')
    L = dict(zip(df_l['country'].to_list(), df_l['lockdown'].to_list()))
    P = dict(zip(df_l['country'].to_list(), df_l['population'].to_list()))
    T = dict(zip(df_l['country'].to_list(), df_l['num_testing'].to_list()))
    return L, P, T 


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
    parser.add_argument('-c','--country-name',help='Country name', default='India')
    parser.add_argument('-p','--param',help='Parameter to vary')
    parser.add_argument('-o','--output-dir',help='Output dir', default='results')
    parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')
    parser.add_argument('-g','--gamma-in',help='Parameter 1/gama',type=float,default=7)
    parser.add_argument('-s','--sigma-in',help='Parameter 1/sigma',type=float,default=7)
    parser.add_argument('-a','--alpha',help='Alpha',type=float,default=1)


    args = parser.parse_args()

    L, P, T = read_lockdown (args)

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
      a.set_xlim(-1,53)
      a.set_ylim(-8.0,11.0)

    plt.subplots_adjust(wspace=0, hspace=0)

    count = 0
    for country in countries:

        R = Reconstruct(args, country)
        R.solve(args.gamma_in, args.sigma_in,args.alpha)
        dates = R.dates  

        y = R.beta 
        days = np.array([i for i in range (0, y.shape[0])])
        lockdown = L[country]

        a = arrow.get(dates[0])
        b = arrow.get(lockdown)
        l = str(b-a).split(" ")[0]
      
        print(count+1,'&',country,'&', P[country],'&', T[country], '&', dates[0], '&', lockdown,' \\\ \hline') 

        ax[count].set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)

        if count % 2==  0: 
            ax[count].set_ylabel('Raw '+ r'$\beta$(t)',fontsize=fontsize)
         
        if count %2 !=0:
            ax[count].yaxis.tick_right()

        if count == 0 or count == 2: 
            ax[count].tick_params(labelbottom=False) 
 
        xx , yy = days[:-2], y[:-2]

        ax[count].axvline(x=float(l),c='k',ls='--')
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
       
