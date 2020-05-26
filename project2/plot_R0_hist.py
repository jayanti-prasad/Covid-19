import sys
import os
import argparse 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib


font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['axes.linewidth'] = 2.0


if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file', help='Input file')
   parser.add_argument('-o','--output-dir', help='Input dir')
   args = parser.parse_args()

   df = pd.read_csv(args.input_file)

   columns = list(df.columns[1:7])

   fig = plt.figure(figsize=(18,15))

   ax = [] 
   ax.append(fig.add_subplot(321))
   ax.append(fig.add_subplot(322))
   ax.append(fig.add_subplot(323))
   ax.append(fig.add_subplot(324))
   ax.append(fig.add_subplot(325))
   ax.append(fig.add_subplot(326))

   count = 0
   for column in columns:
      R = df[column]
      R = R [ R < 10.0]
      R = R [ R > 0.1]
      R = np.log(R)
      ax[count].hist(R)
      ax[count].text(.3,.8,column,
        horizontalalignment='center',
        transform=ax[count].transAxes)
      ax[count].set_xlabel(r'$\log (\mathfrak{R}(t))$')
      count +=1
   #plt.show() 
   plt.savefig(args.output_dir + os.sep + "R0_hist.pdf")

