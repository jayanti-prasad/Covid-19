import numpy as np
import matplotlib.pyplot as plt

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

if __name__ == "__main__":


    t = np.arange(0,100,0.5)
    print(t)

    beta, gamma  = 2.1, 0.1
 
    N = 1000 
    St = [100]
    It = [2.0]
    Rt = [0.0]  
    dt = 0.5  
    for i in range (1, len(t)):
       y = St[i-1], It[i-1], Rt[i-1] 
       dSdt, dIdt, dRdt = deriv(y, t, N, beta, gamma)
       St.append (St[i-1] + dSdt * dt)          
       It.append (It[i-1] + dIdt * dt)          
       Rt.append (Rt[i-1] + dRdt * dt )          
        
      
    plt.plot(t, St,'g')
    plt.plot(t, It,'r')
    plt.plot(t, Rt,'b')
    plt.show() 
