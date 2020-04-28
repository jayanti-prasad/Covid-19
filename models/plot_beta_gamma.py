import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib 

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)


if __name__ == "__main__":

   df1 = pd.read_csv("results_fitting_cut_10/best_fit_params.csv")
   df2 = pd.read_csv("results_fitting_cut_25/best_fit_params.csv")
   df3 = pd.read_csv("results_fitting_cut_100/best_fit_params.csv")


   fig = plt.figure(figsize=(8,8))
   ax = fig.add_subplot(111)
   ax.set_xlabel(r'$\beta$')
   ax.set_ylabel(r'$\gamma$')

   colors = ['red','blue','green']
   cuts = [10, 25, 100]

   count = 0
   for df in [df1, df2, df3]:
      X = df['R0'].to_numpy() 
      Y = df['gamma'].to_numpy() 
      Z = X * Y 
      ax.plot(Z,Y,'o',c=colors[count],label="cut=" + str(cuts[count]))
      count +=1

   ax.plot(Z,Z,label=r'$\beta=\gamma$')      
   plt.legend() 
   plt.savefig("results_R0/beta_gamma.pdf")

  
