import matplotlib.pyplot as plt
import numpy as np


def get_beta (beta0,t0,tw,t):
   rho  = 0.75 
   beta = lambda x : 1.0 - rho * (t-t0)/t

   if t > t0 and t < t0+tw  :
      beta_t = beta0
   else :
      beta_t = beta (t)
   return beta_t


if __name__ == "__main__":

   x = np.arange(0,160,0.5)
   y = np.zeros ([x.shape[0]])

   #for i in range(0, x.shape[0]):
   #   if x[i] > t0 and x[i] < 2 *t0 :
   #      y[i] = beta0
   #   else :
   #      y[i] = beta (x[i])   
  
   beta0,t0,tw = 2.3, 30, 21 

   y = [get_beta (beta0,t0,tw,i) for i in x]

   plt.plot(x,y)
   plt.show()
