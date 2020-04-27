import matplotlib.pyplot as plt
import time
import random
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from model_sir import deriv 
import argparse

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-n', '--num-people', help='Number of people', type=int, default=1000)
   parser.add_argument('-b', '--beta', help='S decay param', type=float, default=0.2)
   parser.add_argument('-g', '--gamma', help='R growth param', type=float, default=0.1)
   args = parser.parse_args()

   N, beta, gamma = args.num_people, args.beta, args.gamma   
   I0, R0 = 1, 0 
   S0 = N - I0 - R0

   plt.show()

   fig = plt.figure(figsize=(6,6))

   ax = plt.subplot(111)

   ax.set_xlim(0, 160)
   ax.set_xlabel("time")
   ax.set_ylabel("S(t), I(t), R(t)")
 
   y0 = S0, I0, R0

   for i in range(10, 160):
      t = np.linspace(0, i, i)
      ret = odeint(deriv, y0, t, args=(N, beta, gamma))
      S, I, R = ret.T

      ax.plot(t, S,'g-',label='Susceptible') 
      ax.plot(t, I,'r-', label='Infected')
      ax.plot(t, R,'b-',label='Recovered with immunity')
      plt.draw()
      plt.pause(1e-17)
      time.sleep(0.1)
      plt.clf()

   # add this if you don't want the window to disappear at the end
   plt.show()

