import sys
import os
import argparse 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import common_utils as cu 
import matplotlib

font = {'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 22}
matplotlib.rc('font', **font)
fcountries=['China','SK','Uruguay']


def show_fitting(cfg, L, N, country):

   skip_days = 4 
   plot_dir = cfg.output_dir() + os.sep + "plots"
   os.makedirs(plot_dir, exist_ok=True)

   data = L.data  
   dates = list(data.index)
   days = [int(i) for i in range(0, data.shape[0])]

   dates_all = dates + cu.get_dates (dates[-1], cfg.num_days_predict())
   days_all = [int(i) for i in range(0, len(dates_all))]

   sir = L.predict (cfg.num_days_predict())
 
   fig = plt.figure(figsize=(15,10))
   ax = fig.add_subplot(111)
   ax.set_title(country)

   ax.set_ylim(10, 10.0 * np.max(data['infected'].to_numpy()))

   ax.scatter(days, data['infected'].to_numpy(), c='b',label='Data')

   if cfg.epd_model() == 'SIR':
       ax.plot(days_all,sir.y[1,:],c='b')
       ax.scatter(days, data['removed'], c='g',label='Data')
       ax.plot(days_all,sir.y[2,:],c='g')

   if cfg.epd_model() == 'SIRD':
      ax.plot(days_all,sir.y[1,:],c='b')
      ax.plot(days_all,sir.y[2,:],c='g')
      ax.plot(days_all,sir.y[3,:],c='r')
      ax.scatter(days, data['deaths'].to_numpy(), c='r',label='Data')
      ax.scatter(days, data['recovered'].to_numpy(), c='g',label='Data')

   if cfg.epd_model() == 'SEIR':
      ax.plot(days_all,sir.y[2,:],c='b')
      ax.plot(days_all,sir.y[3,:],c='g')
      ax.scatter(days, data['removed'].to_numpy(), c='g',label='Data')

   ax.set_yscale('log')
   dates_all = cu.strip_year(dates_all)
   labels = [ dates_all[i] for i in range(0, len(days_all))  if i% skip_days == 0]
   plt.xticks(np.arange(0,len(days_all),skip_days), labels)
   plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
   plt.savefig(plot_dir + os.sep +  country + ".pdf")
   #plt.show()


