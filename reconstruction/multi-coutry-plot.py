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

fontsize = 20 
matplotlib.rc('xtick', labelsize=fontsize) 
matplotlib.rc('ytick', labelsize=fontsize) 
matplotlib.rcParams['axes.linewidth'] = 1.0 


if __name__ == "__main__":

    files = glob.glob(sys.argv[1] + os.sep + "*.csv")

    df_l = pd.read_csv('../data/covid-19-lockdown.csv')

    L = dict(zip(df_l['country'].to_list(), df_l['lockdown'].to_list()))

    fig = plt.figure(figsize=(14,18))

    ax = []
    ax.append(fig.add_subplot(321))
    ax.append(fig.add_subplot(322))
    ax.append(fig.add_subplot(323))
    ax.append(fig.add_subplot(324))
    ax.append(fig.add_subplot(325))
    ax.append(fig.add_subplot(326))

    for a in ax:
      a.set_xlim(-1,55)
      a.set_ylim(-3.5,10.0)
      #a.set_yticklabels([])

    plt.subplots_adjust(wspace=0, hspace=0)

    count = 0
    for f in files:

      y = pd.read_csv(f)['beta'].to_numpy()
      dates = pd.read_csv(f)['date'].to_numpy()
      days = np.array([i for i in range (0, y.shape[0])])
      print("num data points:",y.shape)

      # now get the lockdown day 
      fname = os.path.basename(f).split('_')
      country = fname[0]
      lockdown = L[country]

      a = arrow.get(dates[0])
      b = arrow.get(lockdown)
      l = str(b-a).split(" ")[0]
      
      print("country",country,"lockdown",lockdown,l)

      # now set the limits & labels 
  
      ax[count].set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)
      #ax[count].set_ylim(-5,6)
      #ax[count].set_xlim(1,45)


      if count % 2==  0: 
         ax[count].set_ylabel('raw '+ r'$\beta$(t)',fontsize=fontsize)
         
      if count %2 !=0:
      #  ax[count].set_yticks([])
         ax[count].yaxis.tick_right()

      if count == 0 or count == 2: 
         ax[count].tick_params(labelbottom=False) 
 
      xx , yy = days[:-2], y[:-2]
      #xx = strip_year(xx)
      print("xx=",xx)
      ax[count].axvline(x=float(l),c='k',ls='--')
      ax[count].axhline(y=0,c='k',ls='--')

      ax[count].plot(xx,yy,lw='2',label=country)
      ax[count].scatter(xx,yy)

      plt.setp(ax[count].get_xticklabels(), rotation=90, horizontalalignment='right')
      ax[count].legend(fontsize=fontsize)
      ax[count].xaxis.set_minor_locator(AutoMinorLocator())
      ax[count].xaxis.grid(True, which='both')
      count +=1
      

    plt.savefig(sys.argv[1] + os.sep + "multi_countries.pdf")
    plt.show()
       
