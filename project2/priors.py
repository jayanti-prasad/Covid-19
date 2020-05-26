import numpy as np
from PyCov19.tcoeff import get_tcoeff 

def priors (df, epd_model, beta_model):
 
    dfc = get_tcoeff (epd_model, df)

    dfc = dfc.replace(np.nan, 0)
    
    beta = dfc['beta']
    gamma = dfc['gamma']
    delta = dfc['delta']

    beta  = beta [beta > 0]
    gamma  = gamma [gamma > 0]
    delta  = delta [delta > 0]

    beta_start = np.max ([beta[0], 1.0])
    beta_end   = np.min ([beta[-1], 0.01])

    if beta_model == 'exp':
       alpha = np.max ([beta_end / beta_start,0.01]) 
     
    if beta_model == 'tanh':
       alpha = 1.0 - beta_end / beta_start 
       alpha = np.max ([0.5,alpha])


    gamma  = {'min': np.min(gamma), 'max': np.max(gamma), 'start': np.median (gamma)}  
    delta  = {'min': np.min(delta), 'max': np.max(delta), 'start': np.median (delta)}  
    beta_0 = {'min': np.min(beta), 'max': np.max(beta), 'start': np.median (beta)}  

    mu = {'min': 0.01, 'max':1.0, 'start': 0.1}

    #alpha = {'min': 0.001, 'max': 1.0, 'start': alpha}
    #tl = {'min': 0.0, 'max': df.shape[0], 'start': 1}

    alpha = {'min': 0.0, 'max': 0.0, 'start': 0.0}
    tl = {'min': 0.0, 'max': 0, 'start': 10000.0}

    starting_point = gamma['start'], beta_0['start'], alpha['start'], mu['start'], tl['start']
    bounds = [(gamma['min'], gamma['max']), (beta_0['min'], beta_0['max']), (alpha['min'], alpha['max']),
          (mu['min'], mu['max']), (tl['min'], tl['max'])]


    if epd_model == 'SIRD':
       starting_point = gamma['start'], delta['start'], beta_0['start'], alpha['start'], mu['start'], tl['start']
       bounds.insert(1,(delta['min'], delta['max']))

    return starting_point, bounds  
 
