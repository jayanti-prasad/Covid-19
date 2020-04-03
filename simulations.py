import matplotlib.pyplot as plt
import time
import random
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from sir_solver import deriv 
import argparse


class Population:
    def __init__(self, n_s, n_i, n_r):
        self.ns = n_s
        np.random.seed (seed = 192) 
        self.ni = n_i
        self.nr = n_r
        self.nt = n_s + n_i + n_r 
        self.df = pd.DataFrame (columns=["pos_x","pos_y","type"])
        self.initialize() 

    def initialize (self):
        X = np.random.random([self.nt, self.nt])
        y = np.zeros([self.nt])
        self.df = pd.DataFrame (columns=["pos_x","pos_y","type"])

        for i in range (0, self.nt):           
           if i <= self.ns:
               y[i] = 0
           if i > self.ns and i < self.ns + self.ni :
               y[i] = 1
           if i >= self.ns + self.ni :
               y[i] = 2
 
        self.df["pos_x"] = X[:,0] 
        self.df["pos_y"] = X[:,1] 
        self.df["type"] = y 
 

    def evolve (self):
        #for index, row in self.df.iterrows():
        #    self.df.at[index,'type'] = np.random.randint(2)
        y = np.random.randint(3,size=[self.df.shape[0]])
        self.df['type'] = y   



if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-n', '--num-people', help='Number of people', type=int, default=1000)

   plt.show()

   fig = plt.figure(figsize=(6,6))

   ax = plt.subplot(111)
   #ax2.legend()

   ax.set_xlim(0, 1)
   ax.set_ylim(0, 1)

   for i in range(1, 10):
      X = np.random.random([20,20])
 
      #ax2.plot(t, S,'r-',label='Susceptible') 
      #ax2.plot(t, I,'g-', label='Infected')
      #ax2.plot(t, R,'b-',label='Recovered with immunity')
      ax.scatter (X[:,0],X[:,1]) 

      plt.draw()
      plt.pause(1e-17)
      time.sleep(0.1)
 
   # add this if you don't want the window to disappear at the end
   plt.show()

