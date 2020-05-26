import os
import sys
import argparse  
import configparser
import config
import numpy as np
import pandas as pd 

from PyCov19.beta_models import  exp, tanh
from PyCov19.epidemiology import Epidemology
from PyCov19.epd_models import SIR,SIRD,SEIR 
from PyCov19.optimizer import Learner 
from PyCov19.reproduction import reproduction_number  

from data_utils import get_country_data, get_fitting_data
from cov_utils import  get_population,get_top_countries
from plot_utils import show_fitting 
from priors import priors 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PyCov')
    parser.add_argument('-c', '--config', help='Config file path', required=True)
    parser.add_argument('-e', '--erase', help='Clean previous run data', action='store_true')
    
    args = parser.parse_args()

    cfg_parser = configparser.ConfigParser()
    cfg_parser.read(args.config)

    cfg = config.Config(cfg_parser)

    with open (cfg.output_dir() + os.sep + "params.ini","w") as fp:
        cfg_parser.write(fp)


    df = pd.read_csv(cfg.input_file())
    df_p = pd.read_csv(cfg.population_file())

    os.makedirs(cfg.output_dir(), exist_ok=True)

    countries = get_top_countries(df, cfg.num_countries())

    dF = pd.DataFrame(columns=cfg.columns())
    #countries=['Italy']

    count = 0
    for country in countries:
        try:
           df1, data, init_val = get_fitting_data(df, country,\
              cfg.epd_model(),cfg.num_min_infect())
           N = get_population(country, df_p)
        except:
           print("Could not get data for:",country,"skipping")
           continue 

        dates = data.index 
        if len(dates) < 50 or df1.iloc[-1]['confirmed'] < 10000:
           continue 

        init_val.insert(0, N)

        Y0 = data.iloc[0].to_list() 
        YF = data.iloc[-1].to_list() 
    
        D = {'country': country,'population': "%d" % N,\
            'starting_date': dates[0],'num_days': len(dates)}
        L = Learner(eval(cfg.epd_model()), eval(cfg.beta_model()))

        kwargs = {'N':N,'Y0':Y0}

        #L.initialize  (cfg.starting_point(), cfg.bounds(),**kwargs)
        #try:
        starting_point, bounds  = priors (df1, cfg.epd_model(), cfg.beta_model())
        L.initialize  (starting_point,bounds,**kwargs)
        #except:
        #   print("using default priors")
        #   L.initialize  (cfg.starting_point(), cfg.bounds(),**kwargs)
        #   pass 

        opt =  L.fit(data)

        params = ["%.3f" % p for p in L.params]  
        if cfg.epd_model() == 'SIR':
            [D['gamma'], D['beta_0'],D['alpha'],D['mu'],D['tl']] = params  
        if cfg.epd_model() == 'SIRD':
            [D['gamma'], D['delta'],D['beta_0'],D['alpha'],D['mu'],D['tl']] = params  


        if cfg.plot_data():
            show_fitting(cfg, L, N, country)
  
        D['loss'] = "%.3f " % opt.fun
        D['convergence'] = opt.success   
        R0 = reproduction_number (cfg.beta_model(), cfg.epd_model(), **D)
        D['R0'] = "%.3f"  % R0

        for key in D.keys():
           if key in cfg.columns() :
              dF.at[count, key] = D.get(key)
        print("row=",count, D)
        count +=1

    dF.to_csv(cfg.output_dir() + os. sep + "fit_params.csv")

