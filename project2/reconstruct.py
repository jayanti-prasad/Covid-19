import os
import argparse  
import numpy as np
import pandas as pd
from common_utils import get_country_data, strip_year 
from rplot import rplot
from PyCov19.tcoeff import get_tcoeff 


DATA_DIR="/Users/jayanti/Projects/GiHub/Covid-19/data/"
input_file=DATA_DIR + os.sep + "covid-19-global.csv"
lockdown_file=DATA_DIR + os.sep + "covid-19-lockdown.csv"


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',default=input_file)
   parser.add_argument('-l','--lockdown-file',help='lockdown file',default=lockdown_file)
   parser.add_argument('-m','--model-name',help='Model name')
   parser.add_argument('-c','--country-name',help='Country name')
   parser.add_argument('-o','--output-dir',help='Output dir')
   parser.add_argument('-f','--flag',type=int,default=0, help='flag')

   args = parser.parse_args()

   df_l = pd.read_csv(args.lockdown_file)   
   dF = pd.read_csv(args.input_file)

   dF['removed'] = dF['recovered'] + dF['deaths']
   dF['infected'] = dF['confirmed'] - dF['removed']
   dF = dF[dF['removed'] > 20]

   df = get_country_data (dF, args.country_name)
   dates = strip_year (df['date'].to_list())
   df.index = dates 

   dfc = get_tcoeff (args.model_name, df)


   if args.model_name == 'SIR':
      dfc['R'] = dfc['beta'] / dfc['gamma'] 
      rplot(args, dfc, df_l)
  
   if args.model_name == 'SIRD':
       
      dfc['Rg'] = dfc['beta']/dfc['gamma'] 
      dfc['Rd'] = dfc['beta'] / dfc['delta']
      dfc['R'] = dfc['beta']/ (dfc['gamma'] +dfc['delta'])
      rplot(args, dfc, df_l)
   

