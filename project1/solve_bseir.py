import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

sigma = 1.0/7.0
gamma = 1.0/7.0

A, B, t_off, t_w  = \
    -0.516191291689738,0.7079634566102306,18.76609327215716,1/0.09882156775085947

data_file = "../data/covid-19-global.csv"
population_file = "../data/world_population.csv"


#### This is data utility section 

def get_population(pop_file, country):
   df_p = pd.read_csv(pop_file)
   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()
   return  P[country]


def get_country_data (df, country):
   df = df.fillna(0) 
   df = df[df['country'] == country] 
   df = date_normalize (df)
   df = df.sort_values(by='date')
   return df

# This function ensures that the date format is the same for all the entries. 
def date_normalize (df):
    dates = df['date'].to_list()
    dates1 = []
    for d in dates:
      dd = d.split('-')
      dates1.append(dd[2]+"-"+dd[0]+"-"+dd[1])
    df['date'] = dates1
    return df

def get_fitting_data (df, country):

   df  = get_country_data (df, country)
   df.index = df['date'].to_list() 

   # You can use any condition you want
   # orginal data is copied and not modified 
 
   df1 = df[df['confirmed'] > 25].copy()
   # This is the data for the first day after condition satisfied
   D = df1.iloc[0]
   print("Date:", D['date'], "\n Confirmed:",\
     D['confirmed'],"\n Recovered:", D['recovered'],"\n Deaths:", D['deaths'])  

   # change if needed  
   removed = df['recovered'] +  df['deaths'] 
   data = df['confirmed'] - removed 
   data = data [ data > 25]
    
   return data, removed
#############################################


def beta_t (t):
    y = A * np.tanh ( (t-t_off) / t_w ) + B
    return y


def SEIR (t, y, N):

   S, E, I, R  = y[0]/N, y[1], y[2], y[3]

   beta = beta_t(t)

   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


def solve_tbseir (t, N, IC):

    Y0 = list (IC) 
    params = N,
 
    solution = solve_ivp(SEIR, [0, t.shape[0]],\
       Y0, t_eval = t, vectorized=True, args=params)

    return solution


def show_fitting (data, sol):

    y_true = data.to_numpy()
    y_pred = sol.y[2,:][:y_true.shape[0]]

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)

    ax.plot(sol.t, data/N,'o',c='b',label='Data')
    ax.plot(sol.t, sol.y[2]/N, c='r',label='Infected')
    ax.legend()

    ax.set_yscale('log',basey=10)
    plt.show()

if __name__ == "__main__":
  
    df = pd.read_csv(data_file)

    N = get_population(population_file, 'Italy')
    data, removed  = get_fitting_data (df, 'Italy')

    I0 = data.iloc[0]
    R0 = removed.iloc[0]
    E0 = (data.iloc[1] + (gamma - 1) * data.iloc[0])/sigma
    S0 =  N - I0 - R0 - E0

    t = np.linspace(0, data.shape[0], data.shape[0]*1)

    IC = S0, E0, I0, R0  

    print("IC=",IC)
 
    sol = solve_tbseir (t, N, IC)

    show_fitting (data, sol)

