import sys
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
from scipy.integrate import odeint

def SIR(y,t,N,beta,gamma): 
    S = y[0]/N
    I = y[1]/N
    R = y[2]/N
    return [-beta*S*I, beta*S*I-gamma*I, gamma*I]



def loss(data, beta, gamma):
    N = 1000
    size = data.shape[0]
    S_0,I_0,R_0=1000,10,0 
    t = t_eval=np.arange(0, size, 1) 
    y0 = [S_0,I_0,R_0] 
    #solution = solve_ivp(SIR, [0, size], Y0, t, vectorized=True, args = P)
    solution = odeint(SIR, y0, t, args=(N, beta, gamma))
    return np.sqrt(np.mean((solution[:,1] - data)**2))

class Learner(object):
    def __init__(self, beta, gamma, data, loss):
        self.beta = beta
        self.gamma = gamma
        self.data = data
        self.loss = loss


    def extend_index(self, index, new_size):
        values = index.values
        current = datetime.strptime(index[-1], '%m/%d/%y')
        while len(values) < new_size:
            current = current + timedelta(days=1)
            values = np.append(values, datetime.strftime(current, '%m/%d/%y'))
        return values

    def predict(self, beta, gamma, data):
        #Predict how the number of people in each compartment can be changed through time toward the future.
        #The model is formulated with the given beta and gamma.
        predict_range = 150
        new_index = self.extend_index(data.index, predict_range)
        size = len(new_index)
        extended_actual = np.concatenate((data['confirmed'].to_list(), [None] * (size - len(data.values))))
        return new_index, extended_actual, solve_ivp(SIR, [0, size], [S_0,I_0,R_0], t_eval=np.arange(0, size, 1))

    def train(self):
        #Run the optimization to estimate the beta and gamma fitting the given confirmed cases.
        data = self.data
        beta, gamma = self.beta, self.gamma  
        optimal = minimize(
            loss,
            [0.001, 0.001],
            args=(beta, gamma),
            method='L-BFGS-B',
            bounds=[(0.00000001, 0.4), (0.00000001, 0.4)]
        )
        beta, gamma = optimal.data
        """
        new_index, extended_actual, prediction = self.predict(beta, gamma, data)
        df = pd.DataFrame({
            'Actual': extended_actual,
            'S': prediction.y[0],
            'I': prediction.y[1],
            'R': prediction.y[2]
        }, index=new_index)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_title(self.country)
        df.plot(ax=ax)
        fig.savefig(f"{self.country}.png")
        """

if __name__ == "__main__":

    df = pd.read_csv('../data/covid-19-global.csv')

    df = df[df['country']==sys.argv[1]]
    data = df['confirmed'].to_numpy()

    print(df.columns)
    print(df.shape)
    print(data)
  
    data1 = loss (0.24,0.42,data)
    print(data1)
  
    beta, gamma = 0.24, 0.24 

    L = Learner(beta,gamma, data,loss)

    #L.train()

    #print(data1.shape)
   


 
