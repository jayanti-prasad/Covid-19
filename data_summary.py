import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse 
import glob
import os

def get_summary (df):

   CONFIRMED = {}
   DEATHS = {}
   RECOVERED = {}

   for index, row in df.iterrows():
       try:
         country = row['Country/Region']
       except:
         country = row['Country_Region']
         pass  

       confirmed = row['Confirmed']
       deaths = row['Deaths']
       recovered = row['Recovered'] 
       if country not in CONFIRMED :
          CONFIRMED[country] = confirmed   
       else :
          CONFIRMED[country] += confirmed   
  
       if country not in DEATHS :
          DEATHS[country] = deaths 
       else :
          DEATHS[country] += deaths

       if country not in RECOVERED:
          RECOVERED[country] = recovered 
       else :
          RECOVERED[country] += recovered
   return CONFIRMED, DEATHS, RECOVERED  
    


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-dir',help='Input data dir')

   args = parser.parse_args()

   dF = pd.DataFrame(columns=["date","country","confirmed","deaths","recovered"])

   count = 0
   if args.input_dir:
      filenames = glob.glob(args.input_dir + os.sep + "*.csv")
      for f in filenames:
          df = pd.read_csv(f)
          C, D, R = get_summary(df)
          date =  os.path.basename(f).replace(".csv","")
          for k in C.keys():
             data = [date, k, C[k], D[k], R[k]]
             dF.loc[count] = data 
             print(count, data)
             count +=1

   dF.to_csv("data/full-data-07-04-2020.csv")
   print(dF.shape)


 
