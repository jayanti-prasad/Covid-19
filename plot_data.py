import os
import sys
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib 
import numpy as np


matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

if __name__ == "__main__":

   df = pd.read_csv(sys.argv[1])
   country = sys.argv[2] 
   print("countries:",set(df['countriesAndTerritories'].to_list()))

   df_in = df[df['countriesAndTerritories'] == country]
   dates = df_in['dateRep'].to_list()
   y = df_in['deaths'].to_list()
   z = df_in['cases'].to_list()
   dates = [dates [len(dates)-i-1] for i in range (0, len(dates))]

   y = [i for i  in reversed(y)]

   y_c = np.cumsum(y) 
   fig,ax = plt.subplots(figsize=(20, 10))
   plt.plot(dates[-30:], y[-30:],label='Number of death')
   plt.plot(dates[-30:], y[-30:],'o')
   plt.plot(dates[-30:], y_c[-30:],label='Number of death till date')
   plt.plot(dates[-30:], y_c[-30:],'o')
   plt.xticks(rotation=90)
   plt.ylabel("Total deaths")
   plt.title(country)
   plt.grid()
   ax.legend()
   plt.savefig("countries" + os.sep + country +".pdf")
