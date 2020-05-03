import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
import argparse 

today = date.today()

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-o','--output-dir',help='Output directory',default='data')
  
   args = parser.parse_args()

   url = "https://en.wikipedia.org/wiki/National_responses_to_the_2019%E2%80%9320_coronavirus_pandemic"
   headers = requests.utils.default_headers()
   req = requests.get(url, headers)
   soup = BeautifulSoup(req.content, 'html.parser')

   table = soup.find("table")
   columns_new = ["id","country","pop_2020","change_yearly",\
      "change_net","change_den","per_sq_km","migrants",\
      "fert_rate","med_age","urban_pop","world_share"]

   output_file = "world_population.csv"
    
   df = pd.DataFrame(columns=columns_new)
   output_rows = []
   count = 0 
   print(columns_new)
   for table_row in table.findAll('tr'):
      columns = table_row.findAll('td')
      output_row = []
      for column in columns:
         output_row.append(column.text)
      output_rows.append(output_row)
      print(output_row)
      data = [output_row[i] for i in range(0, len(output_row))]
      if len(data) > 0:
        print(len(data), len(columns_new))
        #df.loc[count]= data 
      count +=1


   #df.to_csv(args.output_dir + os.sep + output_file)
   #print("output_file:",args.output_dir + os.sep + output_file)
