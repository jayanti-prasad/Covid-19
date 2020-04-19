import numpy as np
import matplotlib.pyplot as plt
from epidemiology import  Epidemology
import argparse 

if __name__ == "__main__":
   """
   This is the driver program 
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('-m','--model',help='Model name [sir, seir]', default='sir')
   parser.add_argument('-s','--sigma',help='sigma',type=float,default=0.1)
   parser.add_argument('-b','--beta',help='Beta',type=float,default=0.21)
   parser.add_argument('-g','--gamma',help='Gamma',type=float,default=0.1)
   parser.add_argument('-n','--population-size',help='Population size',type=int,default=1000)
   args = parser.parse_args()

   N = args.population_size 

   E0, I0, R0 = 10, 5, 1

   if args.model == 'sir':
     M =  Epidemology ('sir','solve_ivp',160)
     M.set_init(N,I0,R0)  
     sir = M.evolve (args.beta, args.gamma)
     plt.title ("SIR Model")
     plt.plot(M.t, sir.y[0], label='Succeptable')
     plt.plot(M.t, sir.y[1], label='Infected')
     plt.plot(M.t, sir.y[2], label='Recovered')


   if args.model == 'seir':
     M =  Epidemology ('seir','solve_ivp',160)
     M.set_init(N,E0,I0,R0)
     seir = M.evolve (args.beta,args.sigma,args.gamma)

     plt.title ("SEIR Model")
     plt.plot(M.t, seir.y[0], label='Succeptable')
     plt.plot(M.t, seir.y[1], label='Exposed')
     plt.plot(M.t, seir.y[2], label='Infected')
     plt.plot(M.t, seir.y[3], label='Recovered')
  
   plt.legend()
   plt.show()
