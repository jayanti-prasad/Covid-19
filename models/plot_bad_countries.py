import pandas as pd
import sys
import matplotlib.pyplot as plt
from common_utils import get_country_data 

if __name__ == "__main__":

   df1 = pd.read_csv(sys.argv[1])
   df1 = df1.sort_values(by='R0',ascending=False)
   countries =  df1['country'].to_list()

   df = pd.read_csv("../data/covid-19-global.csv")  

   D = df1['R0']
   D.index = df1['country'].to_list()


   for country  in countries:
      try:
         df2 = get_country_data (df, country) 

         Y =  df2['confirmed'] - df2['deaths'] - df2['recovered']
         Y = Y [Y > 25]
         X = [int(i) for i in  range(0, Y.shape[0])]

         plt.title(country + ", R0= " + str ("%.4f" % D[country]))
         plt.plot(X,Y,'o')
         plt.plot(X,Y)
         plt.show()
      except:
         pass
