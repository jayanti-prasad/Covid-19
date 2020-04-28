import sys
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import matplotlib 

fontsize = 10
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)


if __name__ == "__main__":

   df1 = pd.read_csv("results_fitting_cut_10/best_fit_params.csv")
   df2 = pd.read_csv("results_fitting_cut_25/best_fit_params.csv")
   df3 = pd.read_csv("results_fitting_cut_100/best_fit_params.csv")

   fig = plt.figure(figsize=(18,18))
   ax = [fig.add_subplot(111)]
   #ax.append(fig.add_subplot(212))

   cuts=[10,25,100]

   for i in range(0, 1):
     count = 0 
     for df in [df1, df2, df3]:
        if i == 0: 
           df = df[df['R0'] > 1.5  ]
        #if i == 1:
        #   df = df[df['R0'] > 2]

        X = df['R0']
        X.index = df['country'].to_list()

        ax[i].scatter(X.index, X.values, label='Cut='+str(cuts[count]))
        count +=1      
        plt.setp(ax[i].get_xticklabels(), rotation=90, horizontalalignment='right')
        ax[i].set_ylabel(r'$R_0$')
        ax[i].axhline(y=1,c='k',ls='--')
        ax[i].grid()
        ax[i].legend()
        ax[i].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        ncol=3, mode="expand", borderaxespad=0.)


   #plt.show()     
   plt.savefig("R0b.pdf")
