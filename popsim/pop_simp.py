import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np 
import argparse

np.random.seed (seed=192)

def pbc (x, xmin, xmax):
   for i in range (0, len(x)):
      if x[i] >= xmax:
         x[i] = x[i] - xmax 
      if x[i] < xmin:
         x[i] = xmax + x[i]
   return x  


class Population :
   def __init__(self,cfg):
      self.cfg = cfg 
      self.ns = cfg.num_succeptable
      self.ni = cfg.num_infected
      self.nr = cfg.num_recovered
      self.nt = self.ns + self.ni + self.nr 
  
      self.X = np.random.random ([self.nt, 2])
      self.y = np.zeros (self.nt)
      for i in range (0, self.nt):
          if i < self.ns:
             self.y[i] = 0
          if i >= self.ns and i <  self.ns + self.ni:
             self.y[i] = 1
          elif i > self.ns +  self.ni:
             self.y[i] =2    

   def evolve (self):

      dx = np.random.normal(0.0, self.cfg.var, self.nt)
      dy = np.random.normal(0.0, self.cfg.var, self.nt)
      self.X[:,0] += dx  
      self.X[:,1] += dy  

      self.X[:,0] = pbc (self.X[:,0], 0, 1) 
      self.X[:,1] = pbc (self.X[:,1], 0, 1) 

      for i in range (0, self.nt):
         r_prob = np.random.random([self.nt])
         for j in range (0, self.nt):
            dx  = self.X[i,0] - self.X[j,0] 
            dy  = self.X[i,1] - self.X[j,1] 
            dr  = np.sqrt (dx*dx + dy *dy)
            if dr > 0.0 and dr  < 0.1:
               if self.y[i] == 0 and self.y[j] == 1:
                  if r_prob[i] < self.cfg.prob_infection:
                     self.y[i] = 1
  
      # 20 % infected will die  
      r_prob = np.random.random([self.nt])
      for i in range (0, self.nt):
         if self.y[i] == 1:
            if  r_prob [i] < self.cfg.prob_recovery:
               self.y[i] = 2  
            #else :
            #   self.y[i] = 0 

      return self.X, self.y 


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--num-succeptable',\
      help='Number of succeptable people',type=int, default=100)
    parser.add_argument('-i', '--num-infected',\
      help='Number of infected people', type=int, default=10)
    parser.add_argument('-r', '--num-recovered',\
      help='Number of recovered people', type=int, default=0)
    parser.add_argument('-a', '--prob-infection',\
      help='Probability of infection', type=float, default=0.1)
    parser.add_argument('-b', '--prob-recovery',\
      help='Probability of recovery', type=float, default=0.1)
    parser.add_argument('-v', '--var',\
      help='Variance of Gaussian fluctuatuions', type=float, default=0.1)


    args = parser.parse_args()

    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    pop_size = args.num_succeptable +\
       args.num_infected + args.num_recovered

    P = Population(args)

    xx = np.arange(0,100)
    yy = xx**2  

    col={'0.0':'g','1.0':'r','2.0':'b'}

    yy_ns = []
    yy_ni = []
    yy_nr = []
    xx_t = [] 
    def animate(i):
       X, y = P.evolve()

       ns = [ i for i in y if i==0]
       ni = [ i for i in y if i==1]
       nr = [ i for i in y if i==2]
       print("ns=",len(ns), "ni=", len(ni), "nr=",len(nr)) 
       xx_t.append (i)
       yy_ns.append (len(ns))
       yy_ni.append (len(ni))
       yy_nr.append (len(nr))

       y = [col[str(j)]  for j in y]

       ax1.clear()
       ax2.clear()
       ax1.scatter(X[:,0],X[:,1],marker='.',c=y)
       ax1.set_xlim(0,1)
       ax1.set_ylim(0,1)
       ax1.set_title("Population [Simulation by prasad.jayanti@gmail.com]")
       ax1.set_xticks([])
       ax1.set_yticks([])

       ax2.plot(xx_t, yy_ns,'g-',label='Succeptable')       
       ax2.plot(xx_t, yy_ni,'r-',label='Infected')       
       ax2.plot(xx_t, yy_nr,'b-',label='Recovered/Dead')       
       ax2.set_xlim(0,100)
       ax2.set_ylim(0,pop_size)
       ax2.set_xlabel("time")
       ax2.legend()
       ax2.set_title("Change in population")
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
