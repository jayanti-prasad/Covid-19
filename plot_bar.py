import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import sys
from common_utils import get_country_data

if __name__ == "__main__":

   dF = pd.read_csv(sys.argv[1])

   df1 = get_country_data (dF,'US')
   df2 = get_country_data (dF,'Brazil')
   df3 = get_country_data (dF,'India')
   df4 = get_country_data (dF,'Russia')


   fig = plt.figure(figsize=(12,12))

   ax = fig.add_plot(221)
   bx = fig.add_plot(222)
   cx = fig.add_plot(222)
   dx = fig.add_plot(222)

   
   


