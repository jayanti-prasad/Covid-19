import sys
import numpy as np
import matplotlib.pyplot as plt

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


def lockdown (t, t_start, t_end, dt):

    a = (t-t_start)/dt     
    b = (t-t_end)/dt     
    y = - np.tanh(a) + np.tanh(b)
    return y/2 + 1.0 


def lockdown_exp (mu,sigma,x):
    z = (x-mu)/sigma 
    coeff = (1.0/np.sqrt(2.0*np.pi*sigma*sigma)) 
    return 1.0 - coeff * np.exp (-z*z/2.0)   


if __name__ == "__main__":


    t = np.arange(0,100,0.5)
    l = lockdown (t, 15, 40, 1)

    #l = lockdown_exp (20.0,8.0,t)

    
    #plt.plot(t,l)
    #plt.show() 
    
    #sys.exit()

    beta, gamma  = 2.1, 0.1
 
    N = 1000 
    St = [100]
    It = [2.0]
    Rt = [0.0]  
    dt = 0.5  

    Stl = [100]
    Itl = [2.0]
    Rtl = [0.0]


    for i in range (1, len(t)):
       lkd=l[i]
       #beta *= lkd
       y = St[i-1], It[i-1], Rt[i-1] 
       dSdt, dIdt, dRdt = deriv(y, t, N, beta, gamma)
       St.append (St[i-1] + dSdt * dt)          
       It.append (It[i-1] + dIdt * dt)          
       Rt.append (Rt[i-1] + dRdt * dt )          
       
       y = Stl[i-1], Itl[i-1], Rtl[i-1]
       dSdt, dIdt, dRdt = deriv(y, t, N, beta, gamma)
       Stl.append (Stl[i-1] + lkd * dSdt * dt)
       Itl.append (Itl[i-1] + lkd * dIdt * dt)
       Rtl.append (Rtl[i-1] + lkd * dRdt * dt ) 
 
      
    plt.plot(t, St,'g',label='Succeptable')
    plt.plot(t, Stl,'g:',label='Succeptable [Lockdown]')
    plt.plot(t, It,'r',label='Infected')
    plt.plot(t, Itl,'r:',label='Infected [Lockdown]')
    plt.plot(t, Rt,'b',label='Recovered')
    plt.plot(t, Rtl,'b:',label='Recovered [Lockdown]')
    plt.title("Effect of Lockdown")
    plt.grid()
    plt.legend()
    plt.show() 
