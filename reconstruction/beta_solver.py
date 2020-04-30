import pandas as pd 
import numpy as np

"""
This is the newer version which has better flexibility to 
change sigma and gamma. 

"""

class BetaSolver:

   def __init__(self, df, N):
   
      """
      Read  input data and parse arguments.

      """
      df.index = df['date'].to_list() 
      self.i = df['confirmed']/N
      self.r = df['recovered']/N
      self.d = df['deaths']/N
      self.i = self.i - (self.r + self.d)
      self.size = df.shape[0]
      self.dates = df['date'].to_list()

   def solve (self, gamma_in, sigma_in, alpha):

      """
      SOLVE SEIR equations.  
      """
 
      gamma, sigma, alpha = 1.0/gamma_in, 1.0/sigma_in,alpha 

      rr = pd.Series (np.zeros ([self.size]))
      s =  pd.Series (np.zeros ([self.size]))  # succeptable 
      e =  pd.Series (np.zeros ([self.size]))  # exposed 
      beta = pd.Series (np.zeros ([self.size])) # beta 

      # initial number for the removed 
      rr[0] = (self.r.iloc[0] + self.d.iloc[0]) * alpha 
   
      # Now get the reconstructed ones  
      for j in range(0, self.size-1):
         ii = self.i.iloc[j]
         iip = self.i.iloc[j+1]
         iim = self.i.iloc[j-1]
         e.loc[j] = (iip - ii  + gamma * ii) /sigma

         if j > 0:
            rr.loc[j] = rr.iloc[j-1] + gamma * iim 
         s[j] = 1.0 - (ii + e.loc[j] + rr.loc[j])
      for j in range(0, self.size-1):
         beta.loc[j] = (e.iloc[j+1] - e.iloc[j] \
           + sigma * e.iloc[j])/ (s.iloc[j] * self.i.iloc[j])

      beta.index = self.i.index 
      return beta  
 
