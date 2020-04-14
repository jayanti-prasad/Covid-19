import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob 
import matplotlib 
import numpy as np
from common_utils import get_country_data,strip_year
import arrow

fontsize = 20 
matplotlib.rc('xtick', labelsize=fontsize) 
matplotlib.rc('ytick', labelsize=fontsize) 
matplotlib.rcParams['axes.linewidth'] = 1.0 


if __name__ == "__main__":

    files = glob.glob(sys.argv[1] + os.sep + "*.csv")

    df_l = pd.read_csv('../data/covid-19-lockdown.csv')

    L = dict(zip(df_l['country'].to_list(), df_l['lockdown'].to_list()))

    fig = plt.figure(figsize=(10,18))

    ax = []
    ax.append(fig.add_subplot(321))
    ax.append(fig.add_subplot(322))
    ax.append(fig.add_subplot(323))
    ax.append(fig.add_subplot(324))
    ax.append(fig.add_subplot(325))
    ax.append(fig.add_subplot(326))

    for a in ax:
      a.set_xlabel([])
      #a.set_yticklabels([])

    plt.subplots_adjust(wspace=0, hspace=0)



    count = 0
    for f in files:
      ax[count].set_xlim(0,45)
      ax[count].set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)
      if count % 2==  0: 
         ax[count].set_ylabel('raw '+ r'$\beta$(t)',fontsize=fontsize)
         
      if count %2 !=0:
         ax[count].set_yticks([])

      if count == 0 or count == 2: 
         #ax[count].set_xticks([])
         ax[count].tick_params(labelbottom=False) 


      y = pd.read_csv(f)['beta'].to_numpy()
      dates = pd.read_csv(f)['date'].to_numpy()
      xx = [float(i) for i in range(0, y.shape[0])]
      xx = np.array(xx)
      fname = os.path.basename(f).split('_')
      country = fname[0]  
      lockdown = L[country]

      a = arrow.get(dates[0])
      b = arrow.get(lockdown)
      l = str(b-a).split(" ")[0]

      print("country",country,"lockdown",lockdown,l)
      print("dates",dates)
      ax[count].axvline(x=float(l),c='k',ls='--')
      ax[count].plot(xx,y,lw='2',label=country)
      ax[count].scatter(xx,y)
      ax[count].legend()
      count +=1
      

    plt.savefig(sys.argv[1] + os.sep + "multi_countries.pdf")
    plt.show()
       