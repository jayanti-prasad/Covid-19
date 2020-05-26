import os
import sys
import argparse 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib 
import numpy as np
from data_utils import get_country_data


fontsize = 8
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-file', help='Input file')
    parser.add_argument('-d','--input-dir', help='Input dir')
    parser.add_argument('-o','--output-dir', help='Input dir')

    args = parser.parse_args()

    dF = pd.read_csv (args.input_file)
    df = pd.read_csv (args.input_dir + os.sep + "MODEL1_SIR_exp/fit_params.csv" )
 
    countries = df['country'].to_list()
 
    fig = plt.figure(figsize=(12,18))
    col = 1
    for c in countries:

        df = get_country_data (dF, c)
        x = [int(i) for i in range(0, df.shape[0])]
        y = df['confirmed'] -df['deaths'] -df['recovered']
        if col < 46:
           ax = fig.add_subplot(9,5,col)
           ax.plot(x,y) 
           ax.set_title(c, fontsize=fontsize)
           ax.set_xticks([])
           ax.set_yticks([])
           col +=1
        else:
           break 

    plt.savefig(args.output_dir+"countries.pdf")


