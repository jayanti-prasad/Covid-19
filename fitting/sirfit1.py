import numpy as np
from scipy.integrate import odeint
from scipy.integrate import solve_ivp


def SIR(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


if __name__ == "__main__":

   N = 1000
   I0, R0 = 1, 0
   # Everyone else, S0, is susceptible to infection initially.
   S0 = N - I0 - R0

   # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
   beta, gamma = 1.0/7, 1.0/7.0

   # A grid of time points (in days)
   t = np.linspace(0, 160, 160)

   # Initial conditions vector
   y0 = S0, I0, R0
   # Integrate the SIR equations over the time grid, t.
   ret = odeint(SIR, y0, t, args=(N, beta, gamma))
   #scipy.integrate.odeint(func, y0, t, args=())

   S, I, R = ret.T

   sol = solve_ivp(SIR, [10,20],  y0, args = (N, beta, gamma))
   #scipy.integrate.solve_ivp(fun, t_span, y0)





