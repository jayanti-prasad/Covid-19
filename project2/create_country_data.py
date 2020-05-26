import os
import sys
import argparse
import pandas as pd
import numpy as np
from create_R0_table import print_header, print_footer


if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file', help='Input file')
   parser.add_argument('-o','--output-dir', help='Input dir')
   args = parser.parse_args()

   df = pd.read_csv(args.input_file)

   cols = ['country', 'starting_date','num_days','population']
   tcols = ['country', 'starting\\_date','num\\_days','population']

   count = 0
   fp = open (args.output_dir + os.sep + "countries.tex","w")
   print_header(fp, ['S. No'] + tcols)
   for index, row in df.iterrows():
      data = [count+1] + [row[c] for c in cols]
      data[1] = "{\\bf " + str(data[1]) + "}"
      data[-1] = f"{data[-1]:,}"
      data_row = " & ".join([str(d) for d in data])
      fp.write(data_row + "\\\ \hline\n")
      count +=1
   print_footer (fp,"countries","A summary for the countries used for modelling")
   fp.close()  

