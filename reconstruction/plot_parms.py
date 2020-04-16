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
matplotlib.rcParams['axes.linewidth'] = 2.0 


if __name__ == "__main__":

    files = glob.glob(sys.argv[1] + os.sep + "*.csv")
    fname = sys.argv[1].split("/")[-1]
    print("fname:", fname)

    fig = plt.figure(figsize=(18,12))
    ax = fig.add_subplot(111)

    ax.set_xlim(-1,51)
    ax.set_xlabel('Number of days since '+r'$ t_i$',fontsize=fontsize)
    #if sys.argv[2] == 'beta':
    ax.set_ylabel('raw '+ r'$\beta$(t)',fontsize=fontsize)
    #else: 
    #  ax.set_ylabel(sys.argv[2],fontsize=fontsize) 
    ax.axhline(y=0,c='k',ls='--')
   
    
    colors=['r','b','g','k','o']

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

       if fname == "vary_sigma":
          label = r'$1/\sigma=$'+parts[4]
       if fname == "vary_gamma":
          label = r'$1/\gamma=$'+parts[7]

       label = label.replace('0','').replace('.','')   
       ax.plot(x[:-2],y[:-2],label=label,c=colors[count], lw='2')
       ax.scatter(x[:-2],y[:-2],c=colors[count])

       #ax.plot(x,y,label=label, lw='2')
       #ax.scatter(x,y)


       ax.legend(fontsize=fontsize)
       count +=1

    plt.savefig(sys.argv[1] + os.sep + fname +".pdf")
    plt.show()
       
