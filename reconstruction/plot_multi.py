import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob 
import matplotlib 

matplotlib.rc('xtick', labelsize=16) 
matplotlib.rc('ytick', labelsize=16) 
matplotlib.rcParams['axes.linewidth'] = 1.0 


if __name__ == "__main__":

    files = glob.glob(sys.argv[1] + os.sep + "*.csv")

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.set_xlim(0,45)
    ax.set_xlabel('Number of days since '+r'$ t_i$',fontsize=16)
    if sys.argv[2] == 'beta':
       ax.set_ylabel('raw '+ r'$\beta$(t)',fontsize=16)
    else: 
      ax.set_ylabel(sys.argv[2],fontsize=16) 
 
    for f in files[:6]:
       y = pd.read_csv(f)[sys.argv[2]].to_numpy()
       lab = f.replace(sys.argv[1]+"Italy_",'')
       lab = lab.replace(".csv",'')
       parts = lab.split("_")
       print("parts:",parts)
       label = r'$1/\sigma=$'+parts[3]+r', $1/\gamma=$'+parts[6]
       label = label.replace('0','').replace('.','')   
       ax.plot(y,label=label, lw='2')
       ax.legend(fontsize='large')


    plt.savefig(sys.argv[1] + os.sep + sys.argv[2]+".pdf")
    plt.show()
       
