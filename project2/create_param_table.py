import os
import re
import sys
import numpy as np
import argparse 
import configparser
import pandas as pd
import config 
#from epd_models import SIR,SIRD,SEIR 

def get_model(text):
    text = text.lower()
    numbers = re.compile(r'(\d+)')
    text = numbers.sub(r' (\1)', text)
    return text


def sort_dir (data):
   data1 = [d.split('/')[-1] for d in data]
   data2 = [int(re.findall(r'\d+', d)[0]) for d in data1]
   D = dict (zip (data, data2))
   D = dict(sorted([(value,key) for (key,value) in D.items()]))
   return D


def write_table(fp, input_dir, cfg, df):

    parts = input_dir.split('/')
    label = parts[1]
    model_name = get_model (parts[1].split('_')[0].lower().title())

    print("model name=",model_name)
    print("epd model=",cfg.epd_model())
    print("beta model=",cfg.beta_model())

    columns=['gamma', 'beta_0', 'alpha', 'mu', 'tl', 'R0']
    tcolumns=['$\\gamma$', '$\\beta_0$', '$\\alpha$', '$\\mu$', '$t_l$', '\\Rt']

    if cfg.epd_model() == 'SIRD':
       columns.insert(0,'delta')
       tcolumns.insert(0,'$\\delta$')

    count = 0 
    count1 = 0 

    T={'exp':'exponentially decaying '+ r'$\beta (t)$'}
    T['tanh']='Tanh decaying '+ r'$\beta (t)$'

    count = 0
    for  c in columns:
       X = df[c].to_numpy()
       X_min = "%.4f" % np.min (X) + " & "
       X_max = "%.4f" % np.max (X)
       X_aver = "%.4f" % np.mean (X) + " & "
       X_std = "%.4f" % np.sqrt (np.var(X)) + " & "
       X_median = "%.4f" % np.median (X) + " & "
       if X_max > X_min:
          if count == 0:
              fp.write(model_name + ' & ' +str(count1+1) + '&' + tcolumns[count] + \
                "&" + X_aver +  X_std + X_median + X_min + X_max + "  \\\ \cline{2-8}\n")
          else:
              fp.write('&' +str(count1+1) + '&' + tcolumns[count] + \
                "&" + X_aver +  X_std + X_median + X_min + X_max + "  \\\ \cline{2-8}\n")
          


          count1 +=1
       count +=1

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-dir', help='Input dir')
    parser.add_argument('-o','--output-dir', help='Input dir')

    args = parser.parse_args()
    cfg_parser = configparser.ConfigParser()

    models = [ f.path for f in os.scandir(args.input_dir) if f.is_dir() ]
    D = sort_dir (models)
    cols = ["Model ("+str(k)+")" for k in D.keys()]
    paths = [D[k] for k in D]

    fp = open (args.output_dir + os.sep + "params.tex","w")
    columns=['gamma', 'beta_0', 'alpha', 'mu', 'tl', 'R0']
    tcolumns=['$\\gamma$', '$\\beta_0$', '$\\alpha$', '$\\mu$', '$t_l$', '\\Rt']
    measures = ['S.No.', 'Parameter','Aver','Std Dev','Median','Min','Max']
    measures = ["\\bf{"+x+"}" for x in measures]
    fp.write("\\begin{table}\n")
    fp.write("\\begin{small}\n")
    fp.write("\\begin{center}\n")

    fp.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|} \hline\n")
    fp.write("& \multicolumn{7}{c|} {\\bf{Parametes}}  \\\ \cline{2-8}\n")
    fp.write("\\bf{Models} & \\bf{S.No.}  & \\bf{Parameter}&  \\bf{Aver}&  \\bf{Std Dev}&  \\bf{Median}& \\bf{Min}&  \\bf{Max} \\\ \hline\n")
    for model in paths:
       cfg_parser = configparser.ConfigParser()
       cfg_parser.read(model  + os.sep + "params.ini")
       df = pd.read_csv(model + os.sep +"fit_params.csv")
       cfg = config.Config(cfg_parser)
       write_table(fp, model, cfg, df)
       fp.write("\cline{1-8}\n")
    fp.write("\\end{tabular}\n")
    fp.write("\\caption{A summary of the fitting parameters for all the models.}\n")
    fp.write("\\label{params_table}\n")
    fp.write("\\end{center}\n")
    fp.write("\\end{small}\n")
    fp.write("\\end{table}\n")

