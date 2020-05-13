import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp
from scipy.optimize import minimize


sigma = 1.0/7.0
gamma = 1.0/7.0

data_file = "./covid-19-global.csv"
population_file = "./world_population.csv"

def get_population(pop_file, country):
   df_p = pd.read_csv(pop_file)
   P = df_p['pop_2020'].str.replace(",","").astype(int)
   P.index = df_p['country'].to_list()
   return  P[country]

def get_country_data (df, country):
   df = country_normalize(df)
   df = df.fillna(0) 
   #pandas function to fill NaN values
   
   df = df[df['country'] == country] 
# creates a new dataframe with only the data of the countryof interest...
   
   df = date_normalize (df)
   df = df.sort_values(by='date')

# Are there still unnamed columns? 
# If yes, remove them. 
# Also, remove columns with title 'country' 
# because the entry will just be 
# the same for all rows for a chosen country.
   df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
   df = df.loc[:, ~df.columns.str.contains('country')]
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

# This function normalizes the names of countries... 
def country_normalize(df):
   df = df.replace({'United Kingdom': 'UK'}, regex=True)
   df = df.replace({'Korea, South': 'SK'}, regex=True)
   df = df.replace({'Saudi Arabia': 'SaudiArabia'}, regex=True)
   df = df.replace({'United Arab Emirates': 'UAE'}, regex=True)
   df = df.replace({'Dominican Republic': 'DR'}, regex=True)
   df = df.replace({'South Africa': 'SA'}, regex=True)
   df = df.replace({'Czechia': 'Czech'}, regex=True)
   df = df.replace({'Bosnia and Herzegovina': 'BH'}, regex=True)
   df = df.replace({'New Zealand': 'NZ'}, regex=True)
   df = df.replace({'Cote d\'Ivoire': 'CDI'}, regex=True)

   return df


def get_fitting_data (df, country):
   df  = get_country_data (df, country)

   tmp = len(df[ df['confirmed'] - df['recovered'] - df['deaths'] < 25 ])

   removed = df.iloc[tmp,df.columns.get_loc('recovered')] \
           + df.iloc[tmp,df.columns.get_loc('deaths')] 

   dates = df['date'].to_list()
   data = df['confirmed'] - df['recovered'] - df['deaths']
   data.index = df['date'].to_list() 
   # BTW, can't the RHS be simply replaced by 'dates'? 
   
   data = data [ data > 25]
 
   return data, removed


def beta_t (t, A, B, t_off, t_w):
    #A, B = -0.52, 0.70
    #t_off, t_w = 18.90, 10.35
    y = A * np.tanh ( (t-t_off) / t_w ) + B
    #print("inside beta_t function...", y)
    #exit()
    return y

def tbSEIR (t, y, N, A, B, to, tw):
   S, E, I, R  = y[0]/N, y[1], y[2], y[3]
   #sigma = 1.0/7.0
   #gamma = 1.0/7.0
   beta = beta_t(t, A, B, to, tw)
   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]

def solve_tbseir (t, model, N, I0, E0, R0, A, B, to, tw):
    S0 = N - (I0+E0+R0)
    Y0 = [S0, E0, I0, R0]
    params = N, A, B, to, tw 
    solution = solve_ivp(tbSEIR, [0, t.shape[0]], Y0, t_eval = t, vectorized=True, args=params)
    return solution

"""
def tbSEIR (t, y, A, B, to, tw):
   S, E, I, R  = y[0], y[1], y[2], y[3]
   beta = beta_t(t, A, B, to, tw)
   return [-beta*S*I, beta*S*I-sigma*E, sigma*E-gamma*I, gamma*I]


def solve_tbseir (t, model, N, I0, E0, R0, A, B, to, tw):
    I0, E0, R0 = I0/N, E0/N, R0/N
    S0 = 1 - (I0+E0+R0)
    Y0 = [S0, E0, I0, R0]
    params =  A, B, to, tw 
    solution = solve_ivp(tbSEIR, [0, t.shape[0]], Y0, t_eval = t, vectorized = True, args = params)
    return solution
"""


class Optimizer:
    def __init__(self, N, data, model, rem):
       self.rem = rem
       self.model = model
       self.data = data
       self.N = N 
       self.I0, self.R0 = self.data[0], self.rem
       
       """
       self.E0 = self.I0
       
       gamma = 1/7
       sigma = 1/7
       """
       self.E0 = (self.data[1] + (gamma - 1)*self.data[0])/sigma 
       
       self.S0 =  self.N - self.I0 - self.R0 - self.E0 
       
       self.t = np.arange(0, data.shape[0], 1)  # Consider using np.linspace here?      
       #self.t = np.linspace(0, data.shape[0], data.shape[0]*1)

       # The values of (A, B, t_off , t_w) . 
       # A = -0.52 B = 0.70 t_off = 18.90 t_w = 10.35
       self.starting_point =  [-0.7, 1.0, 30, 20]
       self.bounds = [(-0.9, -0.3), (0.5, 1.5), (10,35), (5, 25)]
       self.df_loss = pd.DataFrame(columns=['A','B','t_off','t_w','mse'])
       self.count = 0 

    def fit(self):
       """
       This is the fitting module and you must chose the parameters carefully. 
       """
       optimal = minimize(self.loss, self.starting_point, method='L-BFGS-B', bounds=self.bounds, tol=1e-12)
#       optimal = minimize(self.loss, self.starting_point, bounds=self.bounds, tol=1e-12)
       
       return tuple(optimal.x)
       # What is x here? 
    
    def loss (self, point):
           
        solution = solve_tbseir (self.t, tbSEIR, self.N, self.I0, self.E0, self.R0,\
           point[0], point[1], point[2], point[3])
        # How does the function loss know what are point[0], point[1] etc?
        # Does minimize function decide the next point?

        """
        print(type(solution))
        print(type(solution.y[2]))
        print(solution.y[2].shape)
        print(solution.y[2])
        print("--------------")
        print(solution.y[2]*self.N)
        #exit()
        """

        y =  self.data.to_numpy()
#        loss_value = np.sqrt( np.mean( (solution.y[2] - y)**2 ) )    
        
        print("actual data")
        print(y)
        print("theoretical one")
        print(solution.y[2])
        """
        print(np.log(y))
        print(np.log(solution.y[2]))
        #exit()
        """

        loss_value = np.sqrt( np.mean( ( np.log( y / solution.y[2] ) )**2 ) )
        # This is basically, sqrt( mean ( ( ln ( y_true / y_pred )  )**2 ) )
       
        if (self.count == 0):
            thesolution = solve_tbseir (self.t, tbSEIR, self.N, self.I0, self.E0, self.R0,\
                -0.52, 0.70, 18.90, 10.35)
            loss_thesol = np.sqrt( np.mean( ( np.log( y / thesolution.y[2] ) )**2 ) )
            print("loss value for the solution = ", loss_thesol)

        data =  [point[0], point[1], point[2], point[3], loss_value]
        data = [ "%.6f" %x for x in data] 

        self.df_loss.loc[self.count] = data;
        self.count +=1  

        print(self.count," parameters:", point, "loss:", loss_value)
        

        """
        print("GG's stop")
        exit()
        """

        return loss_value 


def show_fitting (data, country_name, N, A, B, to, tw):
    I0, R0 = data[0], 0
    E0 = I0
    S0 = N - I0 - R0 - E0

    t = np.arange(0, data.shape[0] + 30, 1)
    sol = solve_tbseir (t,tbSEIR,N,I0,E0,R0,A,B,to,tw)
    sol2 = solve_tbseir (t,tbSEIR,N,I0,E0,R0,-0.52,0.70,18.9,10.35)

    y_true = data.to_numpy()
    print(y_true[0])
    print(y_true[-1])
    y_pred = sol.y[2,:][:y_true.shape[0]]
    mse  = np.sqrt(np.mean((y_true - y_pred)**2))
    y_pred_2 = sol2.y[2,:][:y_true.shape[0]]


    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)

        
    ax.set_title(country_name +", A=" + str("%.4f" %A) + \
      ", B=" + str("%.4f" % B) +\
      r', $t_{off}=$' + str("%.4f" % to)+\
      r', $t_w=$' + str("%.4f" % tw)+\
      r'$, \sigma=\gamma=1/7$')
    
    
    ax.plot(O.t,(data/N)/2.303,'o',c='b',label='Data')
    ax.plot(sol.t, sol.y[2]/N, c='r',label='Infected')
    ax.plot(sol.t, sol2.y[2]/N, c='g',label='best fit soln from mathematica')
    ax.legend()
    ax.set_yscale('log')
    plt.show()
    return mse 

if __name__ == "__main__":
  
    df = pd.read_csv(data_file)

    df_out = pd.DataFrame(columns=['country','A','B','t_off','t_w','mse','population'])
    country = 'Italy'
    print("Getting results for only", country)

    N = get_population(population_file, country)
    print("Population = ", N)
     
    print("      ---------------        ")

    data_tmp = get_fitting_data (df, country)
    data = data_tmp[0]
    removed = data_tmp[1]

    print(data.shape)
    print(data.shape[0])

    """
    print(type(data_tmp))
    print(type(data))
    print(type(data_tmp[0]))
    print(type(data_tmp[1]))
    print(data_tmp[1])
    print(data.shape, data.size, data.ndim)
    print(data)
    """
    print("Entering optimizer")
    O = Optimizer(N, data, tbSEIR, removed)

    params = O.fit()
    A, B, to, tw = params
    mse = show_fitting (data, country, N, A,B,to,tw)
#    row = [country, "%.6f" % A, "%.6f" % B,"%.6f" % to,"%.6f" % tw, "%d" % mse, "%d" % N]
    
    row = ["%.6f" % A, "%.6f" % B,"%.6f" % to,"%.6f" % tw]
    print(row)
   
    print("correct answer")
    print("A = -0.52", "B = 0.70", "t_off = 18.90", "t_w = 10.35")

    print("Done")

#DONE

