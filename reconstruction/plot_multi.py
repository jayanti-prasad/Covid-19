import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob 

if __name__ == "__main__":

    files = glob.glob(sys.argv[1] + os.sep + "*.csv")

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.set_xlim(0,45)
    ax.set_xlabel('Number of days since '+r'$ t_i$')
    if sys.argv[2] == 'beta':
       ax.set_ylabel('raw '+ r'$\beta$(t)')
    else: 
      ax.set_ylabel(sys.argv[2]) 
 
    for f in files[:6]:
       y = pd.read_csv(f)[sys.argv[2]].to_numpy()
       lab = f.replace(sys.argv[1]+"Italy_",'')
       lab = lab.replace(".csv",'')
       parts = lab.split("_")
       label = r'$1/\sigma=$'+parts[2]+r', $1/\gamma=$'+parts[5]
       label = label.replace('0','').replace('.','')   
       ax.plot(y,label=label, lw='2')
       ax.legend()


    plt.savefig(sys.argv[1] + os.sep + sys.argv[2]+".pdf")
    plt.show()
       
