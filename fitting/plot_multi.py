import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

if __name__ == "__main__":

    files=["results2/Italy_sigma_0.1129_gamma_0.1429.csv",
       "results2/Italy_sigma_0.1429_gamma_0.1229.csv",
       "results2/Italy_sigma_0.1229_gamma_0.1429.csv",
       "results2/Italy_sigma_0.1429_gamma_0.1329.csv",
       "results2/Italy_sigma_0.1329_gamma_0.1429.csv",
       "results2/Italy_sigma_0.1429_gamma_0.1429.csv",
       "results2/Italy_sigma_0.1429_gamma_0.1129.csv",
       "results2/Italy_sigma_0.1429_gamma_0.1429.csv"]

  
    for f in files:
       y = pd.read_csv(f)[sys.argv[1]].to_numpy()
       lab = f.replace("results2/Italy_",'')
       lab = lab.replace(".csv",'')
       parts = lab.split("_")
       plt.plot(y,label=r'$\sigma=$'+parts[1]+", " +r'$\gamma=$'+parts[3])
       plt.ylabel(sys.argv[1]) 
       plt.xlim(0,45)

    plt.legend()
    plt.savefig("results2" + os.sep + sys.argv[1]+".pdf")
    #plt.show()
       
