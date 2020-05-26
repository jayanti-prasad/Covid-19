import os
import re
import sys
import numpy as np
import argparse 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from create_param_table import get_model
from glob import glob

font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['axes.linewidth'] = 2.0

def sort_dir (data):
   data1 = [d.split('/')[-1] for d in data]
   data2 = [int(re.findall(r'\d+', d)[0]) for d in data1]
   D = dict (zip (data, data2))
   D = dict(sorted([(value,key) for (key,value) in D.items()]))
   #return [D[k] for k in D]
   return D 

def print_header(fp, columns):
   columns = ["\\bf{"+x+"}" for x in columns]
   print("columns=",columns)
   tt = ['c' for i in range(0, len(columns))]
   tt1 = "|".join(tt)  
   fp.write("\\begin{table*}\n")
   fp.write("\\begin{center}\n")
   fp.write("\\begin{tiny}\n")
   fp.write("\\begin{tabular}{|" + tt1 + "|} \\hline\n")
   fp.write(" & ".join (columns) + "\\\ \hline\n")

def print_footer(fp,label,caption):
   fp.write("\\end{tabular}\n")
   fp.write("\\caption{" + caption +"}\n")
   fp.write("\\label{"+label+"}\n")
   fp.write("\\end{tiny}\n")
   fp.write("\\end{center}\n")
   fp.write("\\end{table*}\n")
   

if __name__ == "__main__":


   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-dir', help='Input dir')
   parser.add_argument('-o','--output-dir', help='Input dir')
   args = parser.parse_args()

   models = [ f.path for f in os.scandir(args.input_dir) if f.is_dir() ]

   D = sort_dir (models)

   cols = ["Model ("+str(k)+")" for k in D.keys()]
   paths = [D[k] for k in D] 
     
   fig = plt.figure(figsize=(18,12))
   ax = fig.add_subplot(111)
   colors=['r','b','g','m','k','c']

   dF1 = pd.DataFrame()
   dF2 = pd.DataFrame()
   dF3 = pd.DataFrame()

   for i in range(0, len(paths)):
     df = pd.read_csv(paths[i] + os.sep + "fit_params.csv")
     df.index = df['country'].to_list()

     R0 = df['R0']
     dF1[cols[i]] = R0 
     dF2[cols[i]] = df['loss']
     dF3[cols[i]] =  1.0 / df['gamma']

     x = np.linspace (0, df.shape[0], df.shape[0])
     ax.plot(x, df['loss'],c=colors[i])
     ax.plot(x, df['loss'],'o',c=colors[i],label=cols[i])
     ax.set_yscale('log')
     ax.set_ylabel('loss')
     ax.set_xlabel('Country')
   plt.legend()

   plt.savefig(args.output_dir + os.sep + "loss.pdf")
 
   dF1.index.name='country'
   dF1['Aver'] =  dF1.mean(numeric_only=True, axis=1)
   dF1['StdDev'] = dF1.var(numeric_only=True, axis=1)
   dF1['StdDev'] = np.sqrt (dF1['StdDev'])
   dF1 = dF1.round(3)
   dF1.to_csv(args.output_dir + os.sep + "R0_ALL.csv")

   dF3.index.name='country'
   dF3['Aver'] =  dF3.mean(numeric_only=True, axis=1)
   dF3['StdDev'] = dF3.var(numeric_only=True, axis=1)
   dF3['StdDev'] = np.sqrt (dF3['StdDev'])
   dF3 = dF3.round(3)
   dF3.to_csv(args.output_dir + os.sep + "beta_0_ALL.csv")


   dF2 = dF2.round(3)
   dF2.to_csv(args.output_dir + os.sep + "RMSD_ALL.csv")

   cols1 = cols + ["Aver","StdDev"]

   fp1 = open (args.output_dir + os.sep + "R0.tex","w")
   fp2 = open (args.output_dir + os.sep + "RMSD.tex","w")
   fp3 = open (args.output_dir + os.sep + "beta0.tex","w")

   print_header(fp1, ['S. No','country'] + cols1)
   print_header(fp2, ['S. No','country'] + cols)

   count = 0
   for i in range(0, dF1.shape[0]) :
       row1 = dF1.iloc[i]
       row2 = dF2.iloc[i]
       data1 = [i+1] + [row1[c] for c in cols1]
       data2 = [i+1] + [row2[c] for c in cols]
       data1.insert(1, dF1.index[i])
       data2.insert(1, dF2.index[i])
       data1[1] = "{\\bf " + str(data1[1]) + "}"
       data2[1] = "{\\bf " + str(data2[1]) + "}"

       data_row1 = " & ".join([str(d) for d in data1])
       data_row2 = " & ".join([str(d) for d in data2])

       fp1.write(data_row1 + "\\\ \hline\n")
       fp2.write(data_row2 + "\\\ \hline\n")

   print_footer(fp1,"R0", "Effective reproduction number \\Rt"
         + "  for countries with different models\n")
   print_footer(fp2,"RMSD", "Root mean square deviation " + r'$RMSD$'
         + "for countries with different models\n")
   fp1.close()
   fp2.close()

