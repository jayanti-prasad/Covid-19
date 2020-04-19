import os
import numpy as np
import pyross
import scipy.io
import argparse
import matplotlib.pyplot as plt 

"""
This program demonstrates how to use the Pyross module given at:
https://github.com/rajeshrinet/pyross
"""


# there is no contact structure
def contactMatrix(t):   
   """
   At present just the diagonal matrix  
   """
   return np.identity(M)



def plot_data (output_dir,data,N):
   """
   This is a plotting function.

   """
   x = data ['t'].reshape(data['t'].shape[1])
   y = data ['X']

   S = y[:,0]
   I = y[:,1] + y[:,2]
   R = N-S-I 

   plt.plot(x, S/N,'g',label='Succeptible')
   plt.plot(x, I/N,'r',label='Infected')
   plt.plot(x, R/N,'b',label='Recovered')
   plt.legend()
   plt.savefig(output_dir + os.sep + "sir_solver_pyross_plot.pdf")


if __name__ == "__main__":

   """
   Computes three time dependent variables on the basis of a set 
   of user given parameters.
   All the parameters have been provided default values.
  
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-o', '--output-dir', help='Output dir',default="/tmp/pyross")
   parser.add_argument('-a', '--alpha', help='fraction of asymptomatic infectives', type=float, default=0)
   parser.add_argument('-b', '--beta', help='infection rate', type=float, default=0.2)
   parser.add_argument('-g', '--gamma', help='recovery rate', type=float, default=0.1)
   parser.add_argument('-f', '--fsa', help='the self-isolation parameter', type=float, default=1)
   parser.add_argument('-s', '--gIa', help='Recovery rate of Ia', type=float, default=0.1)
   parser.add_argument('-t', '--gIs', help='Recovery rate of Is', type=float, default=0.1)

   args = parser.parse_args()

   cfg = vars(args)

   os.makedirs(args.output_dir, exist_ok=True)
 
   M = 1                  # the SIR model has no age structure
   Ni = 1000*np.ones(M)   # so there is only one age group 
   N = np.sum(Ni)         # and the total population is the size of this age group

   Ia0 = np.array([0])     # the SIR model has only one kind of infective 
   Is0 = np.array([1])     # we take these to be symptomatic 
   R0  = np.array([0])     # and assume there are no recovered individuals initially 
 
   S0  = N-(Ia0+Is0+R0)    # so that the initial susceptibles are obtained from S + Ia + Is + R = N

   # duration of simulation and data file
   Tf = 160;  Nt=160; filename = 'this.mat'
   print("file_name:",filename)


   # There are multiple models avaliable and here we are using 
   # the most basic one. 
   model = pyross.models.SIR(cfg, M, Ni)

   # Not very different from the sir_solver we lready have.

   # simulate model
   model.simulate(S0, Ia0, Is0, contactMatrix, Tf, Nt, filename)

   # The output is returned in the form of a matlab 'mat' file 
   # and we can convert that to python compatiable dictionary data structure.

   data = scipy.io.loadmat(filename)

   plot_data (args.output_dir, data, N)

