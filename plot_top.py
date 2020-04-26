import sys
import pandas as pd
import matplotlib.pyplot as plt
from common_utils import date_normalize,get_country_data
import matplotlib 

fontsize = 8
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)



def get_top_countries(df, count):
    df = df.replace({'United Kingdom': 'UK'}, regex=True)
    df1 = df.copy()
    df1 = date_normalize (df1)
    df1 = df1.sort_values(by='date')
    last_date = df1.tail(1)['date'].values[0]
    df_top = df1[df1['date'] == last_date]
    df_top = df_top.sort_values(by=['confirmed'],ascending=False)[:count]

    return df_top  



if __name__ == "__main__":

   df = pd.read_csv(sys.argv[1])

   df_top = get_top_countries(df, 50)
   x = [int(i) for i in range(0, 50)] 
   y = df_top['confirmed'].to_list()
   print(x)
   print(y)

   countries = df_top['country'].to_list()
 
   print(countries)
   fig = plt.figure(figsize=(18,18))
   col = 1
   for c in countries:
      dF = get_country_data (df, c)
      x = [int(i) for i in range(0, dF.shape[0])]
      y = dF['confirmed'].to_numpy()
      ax = fig.add_subplot(5,10,col)
      ax.plot(x,y,'g--')
      ax.set_title(c, fontsize=fontsize)
      col +=1
   plt.show()
