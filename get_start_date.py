import sys
import pandas as pd
from common_utils import date_normalize

if __name__ == "__main__":

   df = pd.read_csv(sys.argv[1])

   countries = list(set(df['country'].to_list()))

   print(countries)
     
   for country in countries:
      df1 = df[df['country']==country]
      df1 = date_normalize (df1)
      df1 = df1.sort_values(by='date')
      df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
      found = False 
      for index, row in df1.iterrows():
          if row['confirmed'] > 10 and found  == False:
             print(country, row['date'], row['confirmed'], row['deaths'], row['recovered'])  
             found = True    
