import numpy as np
import matplotlib.pyplot as plt 
import argparse 
import pandas as pd

def deriv(P, X, N):
    # P = [beta, sigma,gamma]
    # X = [S, E, I, R]
    print("X=",X)
    C = np.array([X[0] * X[2]/N,X[1],X[2]])
    A = np.array([[-C[0],0,0],[C[0],-C[1],0],[0,C[1],-C[2]],[0,0,C[2]]])

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
  
    m, N = args.num_days, args.num_pop 
    df = pd.read_csv("../data/India.csv")

    yy = df['confirmed'].to_numpy()
    xx = np.array([int(i) for i in range(0, len(yy))])

    xx = xx[34:54] - xx[34]
    yy = yy[34:54] 

    N = 1.4E9
    I0 = np.min(yy)
    R0 = 0
    E0 = 30
    S0 = N - I0-E0

    count = 0
    print("day-date-confirmed-recovered-deaths")
    for index, row in df.iterrows():
       print(count, row['date'], row['confirmed'], row['recovered'],row['deaths'])
       count +=1


    print("Parameters:", args, np.min(yy))
   
    P = np.array([args.beta,args.sigma,args.gamma])
    X = np.array([S0,E0,I0,R0])
    C = np.array([0.25,0.25,0.25,0.25])

    x = np.zeros([m])
    S = np.zeros([m])
    E = np.zeros([m])
    I = np.zeros([m])
    R = np.zeros([m])
 
    for i in range(0,m):
      dX =  deriv(P, X, N)
      print(dX)
      X  = X + C * dX 
      X [0] += C[0] * dX[0] * N 
      X [1] += C[1] * dX[1] 
      X [2] += C[2] * dX[2]  
      X [3] += C[3] * dX[3]  

      #S[i], E[i], I[i], R[i] = X[0], X[1], X[2], X[3]
      x[i] = i
 
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
 
    ax.set_title(r'$\beta=$'+str(args.beta)\
      + r', $\sigma=$'+str(args.sigma)\
      +r', $\gamma=$'+str(args.gamma)+",N="+str(N)+",S0="+str(S0)+",I0="+str(I0)+",E0="+str(E0)+",R0=0")
    ax.plot(x,N*S,label='Succeptable')
    plt.plot(x,I,label='Infected')
    plt.plot(xx,yy,'o')
    plt.plot(x,R,label='Recovered')
    plt.plot(x,E,label='Exposed')
    plt.legend()
    plt.savefig("SEIR.pdf")
    plt.show()

 
