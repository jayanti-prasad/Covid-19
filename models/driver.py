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

   M =  Epidemology (args.model,'solve_ivp',160)
 
   if args.model == 'sir':
      M.set_init(N,I0,R0)  
      sir = M.evolve (args.beta, args.gamma)
      plt.title ("SIR Model")
      plt.plot(M.t, sir.y[0], label='Succeptable')
      plt.plot(M.t, sir.y[1], label='Infected')
      plt.plot(M.t, sir.y[2], label='Recovered')


   if args.model == 'seir':
      M.set_init(N,E0,I0,R0)
      seir = M.evolve (args.beta,args.sigma,args.gamma)

      plt.title ("SEIR Model")
      plt.plot(M.t, seir.y[0], label='Succeptable')
      plt.plot(M.t, seir.y[1], label='Exposed')
      plt.plot(M.t, seir.y[2], label='Infected')
      plt.plot(M.t, seir.y[3], label='Recovered')

   if args.model == 'seiard':
      E0, I0, A0, RI0, RA0, D0 = 10, 10, 0, 0, 0, 0      
      beta, sigma, gamma, delta, p = 0.46, 0.14, 0.01, 0.01, 0.8

      M.set_init(N, E0, I0, A0, RI0, RA0, D0)
      solution = M.evolve (beta, sigma, gamma, delta, p) 

      plt.title ("SEIARD Model")
      plt.plot(solution.t, solution.y[0], label='S')
      plt.plot(solution.t, solution.y[1], label='E')
      plt.plot(solution.t, solution.y[2], label='I')
      plt.plot(solution.t, solution.y[3], label='A')
      plt.plot(solution.t, solution.y[4], label='Ri')
      plt.plot(solution.t, solution.y[5], label='Ra')
      plt.plot(solution.t, solution.y[6], label='D')

  
   plt.legend()
   plt.show()
