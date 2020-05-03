import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":

   df = pd.read_csv(sys.argv[1])

   df = df.drop_duplicates(['Country/Region'])

   count = 0 
   df1 = pd.DataFrame(columns=['country','date'])
   for index, row in df.iterrows():
       if row['Date'] is not np.nan :  
          date = row['Date'].split('/')
          date = date[2]+"-"+date[1]+"-"+date[0]
          df1.loc[count] = [row['Country/Region'], date] 
          print(count, row['Country/Region'],date) 
          count +=1

   df1.to_csv("lockdown.csv")
