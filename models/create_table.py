import pandas as pd
import numpy as np 

if __name__ == "__main__":

   df1 = pd.read_csv("test_results_R0/cut_10/best_fit_params.csv")
   df2 = pd.read_csv("test_results_R0/cut_25/best_fit_params.csv")
   df3 = pd.read_csv("test_results_R0/cut_100/best_fit_params.csv")

   cuts=[10,25,100]
   count1 = 1 
   print("\\begin{table}")
   print("\\begin{center}")
   print("\\begin{tabular}{|c|c|c|c|c|c|c|} \\hline")
   print("S. NO & ${\\bar R}$ & $\sigma_{R}$ & $I_0$ &  $R^l$ & $R^u$ & Countries \\\ \hline")
   for r in [[0,10],[0.25,6.0]]:
      count = 0
      for df in [df1, df2, df3]:
         l, h = r[0], r[1]
         df = df [df['R0'] > l]  
         df = df [df['R0'] < h]  
         X = df['R0']
         mean = np.mean(X)
         std = np.sqrt(np.var(X))
         num_countries= df.shape[0]
         
         print(count1,"&", "%.4f" % mean,"&", "%.4f" % std,"&", cuts[count], "&", l, "&", h, "&", num_countries,"\\\ \hline")  
         count +=1
         count1 +=1
   print("\\end{tabular}")
   print("\\end{center}")
   print("\\end{table}")





