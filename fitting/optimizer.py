import numpy as np

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

    params = 

