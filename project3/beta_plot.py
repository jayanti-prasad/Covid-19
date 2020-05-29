import os
import sys
sys.path.append("../project2/")
import argparse 
import numpy as np
import pandas as pd

from PyCov19.tcoeff import get_tcoeff 
from data_utils import get_country_data, get_fitting_data
from date_utils import strip_year
from cov_utils import  get_population,get_top_countries
from plot_utils import show_fitting
from plot_frame import plot_frame 
import matplotlib.pyplot as plt 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PyCov')
    parser.add_argument('-i', '--input-file', help='Input file')
    parser.add_argument('-o', '--output-dir', help='Output dir')
   
    args = parser.parse_args()

    dF = pd.read_csv(args.input_file)

    countries=['Italy','US','Spain','India']

    fig = plt.figure(figsize=(18,12))
    ax  = fig.add_subplot(111)


    count = 0  
    for country in countries:
       df = get_country_data (dF, country)
       df = df[df['confirmed']-df['recovered']-df['deaths'] > 25 ]
       if df.shape[0] < 50:
          continue 

       dfc = get_tcoeff ('SIR',df)
       dfc = dfc.replace(np.nan, 0)
   
       dfc.index = strip_year (dfc['date'].to_list())

       beta = dfc['beta']
       beta = beta [beta > 0.0]

       ax.plot(beta,'o',label=country)


    dates = strip_year(df['date'].to_list())
    labels = [ dates[i] for i in range(0, len(dates))  if i% 2 == 0]
    plt.xticks(np.arange(0,len(dates), 2), labels)
    plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')

    plt.legend()

    plt.show()

