import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob 
import matplotlib 
import numpy as np

fontsize = 26 
matplotlib.rc('xtick', labelsize=fontsize) 
matplotlib.rc('ytick', labelsize=fontsize) 
matplotlib.rcParams['axes.linewidth'] = 1.0 


if __name__ == "__main__":

    files = glob.glob(sys.argv[1] + os.sep + "*.csv")
    #files1 = glob.glob(sys.argv[3] + os.sep + "*.csv")

    #files = files + files1

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.set_xlim(0,45)
    ax.set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)
    if sys.argv[2] == 'beta':
       ax.set_ylabel('raw '+ r'$\beta$(t)',fontsize=fontsize)
    else: 
      ax.set_ylabel(sys.argv[2],fontsize=fontsize) 
   
    
    colors=['r','b','g','k','o']

    #files1 = [files[5],files[2],files[0],files[1],files[4]]
    files1 = [files[2], files[0], files[1]]
   
    count = 0
    for f in files1:
       y = pd.read_csv(f)[sys.argv[2]].to_numpy()
       x = [float(i) for i in range(0, y.shape[0])]
       x = np.array(x)
       lab = f.replace(sys.argv[1]+"Italy_",'')
       lab = lab.replace(".csv",'')
       parts = lab.split("_")
       print("parts:",parts)
       label  = r'$1/\sigma=$'+parts[3]# + r', $1/\gamma=$'+parts[6]
       label  = label.replace('0','').replace('.','')   
       ax.plot(x,y,label=label,c=colors[count], lw='2')
       ax.scatter(x,y,c=colors[count])

       #ax.plot(x,y,label=label, lw='2')
       #ax.scatter(x,y)


       ax.legend(fontsize=fontsize)
       count +=1

    plt.savefig(sys.argv[1] + os.sep + sys.argv[2]+".pdf")
    plt.show()
       
