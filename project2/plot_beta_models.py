import sys
import os
import numpy as np
from scipy.integrate import solve_ivp
from PyCov19.beta_models import  exp, tanh,polynom
from PyCov19.epidemiology import Epidemology
from PyCov19.epd_models import SIR

import argparse 
import matplotlib.pyplot as plt 
import matplotlib


font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['axes.linewidth'] = 2.0

if __name__ == "__main__":

   params = [{"beta_0" : 0.35, "alpha" : 0.5, "mu" : 0.5, "tl": 500}]
   params.append({"beta_0" : 0.35, "alpha" : 0.5, "mu" : 1.05, "tl": 10})
   params.append({"beta_0" : 0.35, "alpha" : 0.5, "mu" : 0.1, "tl": 10})
   params.append({"beta_0" : 0.35, "alpha" : 0.5, "mu" : 0.1, "tl": 10})
  
   beta_models = [exp,polynom,tanh,exp] 

   color=['k','r','g','b']
  
   fig = plt.figure(figsize=(12,12))
   ax = fig.add_subplot(211)
   bx = fig.add_subplot(212)

   ax.set_xlabel(r'$t$')
   ax.set_ylabel(r'$\beta(t)$')

   #bx.set_ylabel(r'$S(t),I(t),R(t)$')
   bx.set_xlabel(r'$t$')

   size = 200 

   x = np.arange(0, size, 0.5)
   for i in range (0, len(beta_models)):
      y = [beta_models[i](t, **params[i]) for t in x]
      if i == 0:
         mname = "constant"
      else:
         mname = beta_models[i].__name__
      ax.plot(x,y,c=color[i], label=mname)

   ax.legend()
   #ax.legend(loc='upper center', bbox_to_anchor=(1.11, 1.15),
   #       ncol=4, fancybox=True, shadow=True)

   for i in range (0, len(beta_models)):

      E = Epidemology('ode_solver', SIR, beta_models[i])
      E.set_init(N=1000,Y0=[1,0])
      D = params[i]
      P = [D['beta_0'], D['alpha'], D['mu'], D['tl']] 
      P.insert(0,0.05)
      y = E.evolve (size, P) 

      mname = beta_models[i].__name__ 
      if i == 3:
         mname = "constant "

      if i == 0:
         bx.plot(y.t, y.y[0],'-.', c=color[i],label='S(t)')
         bx.plot(y.t, y.y[1], c=color[i],label='I(t)')
         bx.plot(y.t, y.y[2],':', c=color[i],label='R(t)')
      else:
         bx.plot(y.t, y.y[0],'-.', c=color[i])
         bx.plot(y.t, y.y[1], c=color[i])
         bx.plot(y.t, y.y[2],':', c=color[i])
      bx.legend()
 
   #plt.show()
   plt.savefig("plots" + os.sep + "beta_models.pdf")
 

