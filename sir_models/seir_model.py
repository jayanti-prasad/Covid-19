import numpy as np
import matplotlib.pyplot as plt 
import argparse 

def deriv(P, X, N):
    # P = [beta, sigma,gamma]
    # X = [S, E, I, R]

    c1 = X[0] * X[2]/N  
    c2 = X[1]
    c3 = X[2]

    A = np.array([[-c1,0,0],[c1,-c2,0],[0,c2,-c3],[0,0,c3]])

    Y = np.matmul(A,P) 

    return Y 
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--num-pop',type=int,default=1000,help='Population size')
    parser.add_argument('-d','--num-days',type=int,default=300,help='Number of days')
    parser.add_argument('-b','--beta',type=float,default=2.1,help='Parameter beta ')
    parser.add_argument('-g','--gamma',type=float,default=0.1,help='Parameter gamma')
    parser.add_argument('-s','--sigma',type=float,default=0.2,help='Parameter sigma')

    args = parser.parse_args()

    print("Parameters:", args)
   
    m, N = args.num_days, args.num_pop 
   
    P = np.array([args.beta,args.sigma,args.gamma])
    X = np.array([100.0,1.0,2.0,0.0])
    C = np.array([0.5,0.5,0.5,0.5])

    x = np.zeros([m])
    S = np.zeros([m])
    E = np.zeros([m])
    I = np.zeros([m])
    R = np.zeros([m])
 
    for i in range(0,m):
      dX =  deriv(P, X, N)
      X  = X + C * dX 
      S[i], E[i], I[i], R[i] = X[0], X[1], X[2], X[3]
      x[i] = i
 
   
    plt.title(r'$\beta=$'+str(args.beta)\
      + r', $\sigma=$'+str(args.sigma)\
      +r', $\gamma=$'+str(args.gamma))
    plt.plot(x,S,label='Succeptable')
    plt.plot(x,I,label='Infected')
    plt.plot(x,R,label='Recovered')
    plt.plot(x,E,label='Exposed')
    plt.legend()
    plt.savefig("SEIR.pdf")
    plt.show()

 
