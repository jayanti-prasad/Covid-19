import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def SEIARD (t, y,  N, beta, sigma, gamma, delta, p):

  S, E, I, A, RI, RA, D =\
     y[0], y[1], y[2], y[3], y[4], y[5], y[6]

   
  f = (I-A) / (N-D)
  print("f=",f)
  
  dSdt = -beta * S * f 
  dEdt =  beta * S * f  - sigma * E
  dIdt = p * sigma * E - (delta + gamma ) * I
  dAdt = (1.0 -p ) * sigma * E - gamma * A
  dRidt = gamma * I
  dRadt = gamma * A 
  dDdt  = delta * I

  return  [dSdt, dEdt, dIdt, dAdt, dRidt, dRadt,  dDdt]


if __name__ == "__main__":
   
   N, beta, sigma, gamma, delta, p = 1000, 0.46, 0.14, 0.01, 0.01, 0.8

   E0, I0, A0, RI0, RA0, D0 = 10, 10, 0, 0, 0, 0
 
   S0 = N - (E0 + I0 +  A0 + RI0 + RA0 + D0) 

   Y0 = [S0, E0, I0, A0, RI0, RA0, D0]
   params = N, beta, sigma, gamma, delta, p 
   
   size = 160  
   t = np.arange(0, size, 1)
   print("t=",t)

   solution = solve_ivp(SEIARD, [0, size], Y0,\
            t_eval = t,vectorized=True, args=params)


   plt.plot(solution.t, solution.y[0], label='S')
   plt.plot(solution.t, solution.y[1], label='E')
   plt.plot(solution.t, solution.y[2], label='I')
   plt.plot(solution.t, solution.y[3], label='A')
   plt.plot(solution.t, solution.y[4], label='Ri')
   plt.plot(solution.t, solution.y[5], label='Ra')
   plt.plot(solution.t, solution.y[6], label='D')
   plt.legend()
   plt.show() 
   
