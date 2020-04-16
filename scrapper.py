import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
today = date.today()

if __name__ == "__main__":

   output_dir="data/worldometers"
 
   url = "https://www.worldometers.info/coronavirus/"
   headers = requests.utils.default_headers()
   req = requests.get(url, headers)
   soup = BeautifulSoup(req.content, 'html.parser')

   #html = open("index.html").read()
   #soup = BeautifulSoup(html)
   table = soup.find("table")

   columns=['country','total_cases','new_cases',\
     'total_deaths','new_deaths','total_recovered',\
     'active_cases','serious_critical','total_case_per_mn',\
     'deaths_per_mn','total_test',"tests_per_mn","countinent"]

   output_file = output_dir + os.sep + "covid-19-"+str(today)+".csv"
    
   df = pd.DataFrame(columns=columns)
   output_rows = []
   count = 0 
   for table_row in table.findAll('tr'):
      columns = table_row.findAll('td')
      output_row = []
      for column in columns:
         output_row.append(column.text)
      output_rows.append(output_row)
      print(count, len(output_row), len(columns))
      if count > 8 and count <= 220: 
         df.loc[count]= output_row 
      count +=1

   df.to_csv(output_file)
   print("output_file:",output_file)
