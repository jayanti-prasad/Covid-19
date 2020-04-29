import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

   df1 = pd.read_csv("test_results_tanh/best_fit_params.csv")
   df2 = pd.read_csv("test_results_R0/cut_25/best_fit_params.csv")

   X = df1['R0']
   X.index = df1['country'].to_list()

   Y = df2['R0']
   Y.index = df2['country'].to_list()

   fig = plt.figure(figsize=(18,18))
   ax = fig.add_subplot()

   ax.plot(X,'o',label='tanh' + ", Mean=" + str("%.4f" % np.mean(X)))
   ax.plot(Y,'o',label='exp'  + ", Mean=" + str("%.4f" % np.mean(Y)))
   ax.set_ylabel(r'$R_0$')
   ax.axhline(y=1,c='k',ls='--')
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   plt.legend()
   plt.show()
  
 
