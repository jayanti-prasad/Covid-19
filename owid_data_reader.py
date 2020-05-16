import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from common_utils import strip_year 

data_file="/Users/jayanti/Data/COVID-19/covid-19-data/public/data/owid-covid-data.csv"

if __name__ == "__main__":

   dF = pd.read_csv(data_file)

   print(dF.shape)
   print(dF.columns)
   
   df = dF[['location','date','total_cases','total_deaths','total_tests','population','median_age']]

   print(df.shape)
   df.to_csv("data/covid-19-global-owid.csv")

   data = df[df['location']==sys.argv[1]]
   dates = strip_year (data['date'].to_list())
   data.index = dates 

   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot(111)

   ax.plot(dates[1:], data['total_cases'].iloc[1:])

   plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
   labels = [dates[i] for i in range(1, len(dates))  if i% 3 == 0]
   plt.xticks(np.arange(1,len(dates),3), labels)
   ax.grid()
   plt.show()
