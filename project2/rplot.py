import os
import argparse  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from date_utils import   strip_year, get_date_diff 
from data_utils import get_country_data
from cov_utils import get_lockdown_day
import matplotlib


font = {'family' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['axes.linewidth'] = 2.0



def rplot(args, df, dfl):

   fig = plt.figure(figsize=(18,12))

   ax = fig.add_subplot(311)
   bx = fig.add_subplot(312)
   cx = fig.add_subplot(313)


   ax.set_title(args.country_name)
   

   if args.flag < 2:
      ax = fig.add_subplot(311)
      bx = fig.add_subplot(312)
      cx = fig.add_subplot(313)

   if args.flag == 0:
     ax.set_ylabel(r'$\beta(t)$')
     bx.set_ylabel(r'$\gamma(t)$')
     cx.set_ylabel(r'$\mathfrak{R}(t)$')
   
    
   if args.flag == 1:
      ax.set_ylabel(r'$\beta(t)$')
      bx.set_ylabel(r'$\gamma(t)$')
      cx.set_ylabel(r'$\delta(t)$')

   
   if args.flag == 2:
      ax.set_ylabel(r'$\mathfrak{R}_\gamma(t)$')
      bx.set_ylabel(r'$\mathfrak{R}_\delta(t)$')
      cx.set_ylabel(r'$\mathfrak{R}(t)$')


   first_date = df.index[0] 
   lday = get_lockdown_day(first_date, dfl, args.country_name)

   dates = strip_year(df['date'].to_list())

   labels = [ dates[i] for i in range(0, len(dates))  if i% 2 == 0]


   ax.set_xticks(np.arange(0,len(dates), 2), labels)
   bx.set_xticks(np.arange(0,len(dates), 2), labels)
   plt.xticks(np.arange(0,len(dates), 2), labels)

   plt.setp(cx.get_xticklabels(), rotation=90, horizontalalignment='right')

   ax.axvline(x=lday,c='r',ls='--')
   bx.axvline(x=lday,c='r',ls='--')
   cx.axvline(x=lday,c='r',ls='--')

   ax.set_xticklabels([])
   bx.set_xticklabels([])

   if args.flag < 2:
      ax.plot(dates, df['beta'],c='b')
      ax.plot(dates, df['beta'],'ob')

      bx.plot(dates, df['gamma'],c='b')
      bx.plot(dates, df['gamma'],'ob')

   if args.flag == 2:
      ax.plot(dates, df['Rg'],c='b')
      ax.plot(dates, df['Rg'],'ob')
      bx.plot(dates, df['Rd'],c='b')
      bx.plot(dates, df['Rd'],'ob')
      cx.plot(dates, df['R'],c='b')
      cx.plot(dates, df['R'],'ob')
      ax.set_yscale('log')
      bx.set_yscale('log')
      cx.set_yscale('log')

   if args.flag == 0:
      cx.plot(dates, df['R'],c='b')
      cx.plot(dates, df['R'],'ob')
      cx.set_yscale('log')

   if args.flag == 1:
      cx.plot(dates, df['delta'],c='b')
      cx.plot(dates, df['delta'],'ob')

   
   cx.grid(which='minor', alpha=0.5)
   cx.grid(which='major', alpha=0.5)

   ax.grid()
   bx.grid()
   cx.grid()
   plt.savefig(args.output_dir + os.sep + "rplot_"+args.country_name +"_"+str(args.flag)+".pdf")
   #plt.show()


