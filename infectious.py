import pandas as pd
import matplotlib.pyplot as plt 
import argparse 
from common_utils import date_normalize 

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input file')
   parser.add_argument('-c','--country-name',help='Country name')
 
   args = parser.parse_args()

   df = pd.read_csv(args.input_file)
   df = df[df['country'] == args.country_name]
   df = date_normalize (df)
   df = df.sort_values(by=['date'],ascending=True)
   print(df.columns)
   
   X = df['confirmed'].to_list()

   Y = [ X[i+1] - X[i] for i in range(0, len(X)-1)]
   t = [ i for i in range(0, len(Y))]

   plt.plot(t,Y)
   plt.scatter(t,Y)
 

   #df['infection'] = df['confirmed'] - df['deaths'] - df ['recovered'] 

   #ax = df.plot(x="date", y="confirmed",color="C1")
   #df.plot(x="date", y="infection",ax=ax, color="C2")
   #plt.xticks(rotation=45)

   plt.show()
