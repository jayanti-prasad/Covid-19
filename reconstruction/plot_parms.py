import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
from reconstruction import Reconstruct

fontsize = 28 
matplotlib.rc('xtick', labelsize=fontsize) 
matplotlib.rc('ytick', labelsize=fontsize) 
matplotlib.rcParams['axes.linewidth'] = 2.0 
matplotlib.rcParams["font.family"] = "Courier New"


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country name')
   parser.add_argument('-p','--param',help='Parameter to vary')
   parser.add_argument('-o','--output-dir',help='Output dir', default='results')
   parser.add_argument('-l','--lockdown-file',help='Lockdown file',\
      default='../data/covid-19-lockdown.csv')

   args = parser.parse_args()
   os.makedirs(args.output_dir, exist_ok=True)

   R = Reconstruct(args, args.country_name)

   if args.param == "gamma":
      gamma = [5,9,14]
      sigma = [9]
      alpha = [1.0]
 
   if args.param == "sigma":
      sigma = [5,9,14]
      gamma = [9]
      alpha = [1.0]

   if args.param == "alpha":
      sigma = [9]
      gamma = [9]
      alpha = [0.2,1.0,5.0]

   if args.param == "all":
      sigma = [5,14,9]
      gamma = [5,14,9]
      alpha = [1.0]
   
   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot(111)
   ax.set_xlim(-1,52)

   ax.set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)
   ax.set_ylabel('Raw '+ r'$\beta$(t)',fontsize=fontsize)

   ax.axhline(y=0,c='k',ls='--')
   colors=['r','b','g','k','y','m','w','g','r']
 
   count = 0  
   for g in gamma:
     for s in sigma:
        for a in alpha:
          R.solve (g, s, a)
          y = R.beta 
          x = np.array([float(i) for i in range(0, y.shape[0])])
          if args.param == 'gamma':
             label = r'$1/\gamma=$' + str(g)
          if args.param == 'sigma':
             label = r'$1/\sigma=$' + str(s)
          if args.param == 'alpha':
             label = r'$\alpha=$' + str(a)
          if args.param == 'all':
             label = ""
             if s== 9 and g == 9:
                color = 'k'
             else :
                color = 'grey'  
          else:
             color = colors[count]     

          ax.plot(x[:-2],y[:-2],label=label,c=color, lw='3')
          ax.scatter(x[:-2],y[:-2],c=color)
          count +=1

   ax.legend(fontsize=fontsize)
   plt.savefig(args.output_dir + os.sep + "vary_" + args.param + ".pdf")
   plt.show()
       
