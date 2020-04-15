import sys
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

def SIR(y,t,P): 
    beta, gamma = P[0], P[1]
    S = y[0]
    I = y[1]
    R = y[2]
    return [-beta*S*I, beta*S*I-gamma*I, gamma*I]



def loss(beta, gamma, data):
    #RMSE between actual confirmed cases and the estimated infectious people with given beta and gamma.
    size = data.shape[0]
    print("beta=",beta,"gamma=",gamma)
    S_0,I_0,R_0=1000,10,0 
    P = [beta, gamma]  
    print("beta=",beta,"gamma=",gamma)
    t = t_eval=np.arange(0, size, 1) 
    Y0 = [S_0,I_0,R_0] 
    solution = solve_ivp(SIR, [0, size], Y0, t, vectorized=True, args = P)

    return solution 
    #return np.sqrt(np.mean((solution.y[1] - data)**2))

"""

class Learner(object):
    def __init__(self, df, country, loss):
        self.country = country
        self.loss = loss

    def load_confirmed(self, country):
      #Load confirmed cases downloaded from HDX
      #country_df = df[df['country'] == country]
      country_df = pd.read_csv("../data/covid-19-Italy.csv",skiprows=24)
      return country_df#.iloc[0].loc[START_DATE[country]:]


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
        data = self.load_confirmed(self.country)
        print("data")
        optimal = minimize(
            loss,
            [0.001, 0.001],
            args=(data),
            method='L-BFGS-B',
            bounds=[(0.00000001, 0.4), (0.00000001, 0.4)]
        )
        beta, gamma = optimal.x
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
   
  


 
