#import sys
#import os
#import argparse 
import numpy as np
#import pandas as pd
from scipy.optimize import minimize
#from datetime import timedelta, datetime
#import matplotlib.pyplot as plt
#from common_utils import get_country_data, strip_year  
#from epidemiology import SIR, SEIR, SEIARD, Epidemology 
from epidemiology import Epidemology 


class Learner(object):
    """
    This is the main optimier class
    """
    def __init__(self, N, data, model):

        self.model = model
        self.data = data 

        I0, R0 = self.data[0], 0  
        S0 =  N - I0 - R0 

        self.E = Epidemology (self.model,'solve_ivp',  data.shape[0])
        self.E.set_init (N, I0, R0)
        print(N, I0, R0, S0)

    def initial_guess (self):

        if self.model == 'sir':
           starting_point =  [0.12, 0.11]
           bounds = [(1.0E-03, 10.0), (1.0E-03, 10.0)]

        if self.model == 'dbsir':
            starting_point = [0.1, 0.01, 0.1]
            bounds = [(0.01, 1.0), (1.0E-4,1.0), (0.01, 1.0)]             

        return starting_point, bounds


    def fit(self):
        """
        This is the fitting module and you must chose the parameters carefully. 

        """
        starting_point, bounds = self.initial_guess() 
        optimal = minimize(self.loss,starting_point, method='L-BFGS-B', bounds=bounds)

        if optimal.success == True:
           return tuple(optimal.x) 
        else:
           print(optimal) 
           return None 

    def loss (self, point):
        if self.model == 'sir':
           solution = self.E.evolve(point[0], point[1])
        if self.model == 'dbsir':
           solution = self.E.evolve(point[0], point[1], point[2])

        y =  self.data.to_numpy()
        return np.sqrt(np.mean((solution.y[1] - y)**2))

