import sys
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import matplotlib 
import argparse 

fontsize = 10
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)

if __name__ == "__main__":

   #df1 = pd.read_csv("test_results_R0/cut_10/best_fit_params.csv")
   df1 = pd.read_csv("test_results_tanh/best_fit_params.csv")
   df2 = pd.read_csv("test_results_R0/cut_25/best_fit_params.csv")
   #df3 = pd.read_csv("test_results_R0/cut_100/best_fit_params.csv")

   fig = plt.figure(figsize=(18,18))
   ax = fig.add_subplot(111) 

   #cuts=[10,25,100]
   cuts=["tanh","exp"]

   count = 0 
   for df in [df1, df2]:
      #df = df [df['R0'] > 0.25]  
      #df = df [df['R0'] < 6.0]  
      X = df['R0']
      X.index = df['country'].to_list()
      print("mean R0=",np.mean(X), "var:", np.sqrt(np.var(X)),df.shape[0])

      ax.scatter(X.index, X.values, label='Cut='+str(cuts[count]))
      count +=1      
      plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
      ax.set_ylabel(r'$R_0$')
      ax.axhline(y=1,c='k',ls='--')
      ax.grid()
      ax.legend()
      ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        ncol=3, mode="expand", borderaxespad=0.)

   plt.show()     
   #plt.savefig("R_tanh_exp.pdf")
