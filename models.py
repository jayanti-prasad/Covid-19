import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
   return a * np.exp(-b * x)   

class ExpModel:
   def __init__(self):
      self.start = 0 
      self.a = None 
      self.b = None 

   def fit(self, x, y):
      for i in range(0, x.shape[0]):
         if self.start == 0 and y[i] > 0:
             self.start = i

      x_fit = x[self.start:]-x[self.start]
      y_fit = y[self.start:]

      popt, pcov = curve_fit(func, x_fit, y_fit)      
  
      self.a, self.b = popt[0], popt[1]

   def predict(self, x):

     y = np.zeros (x.shape[0])
     for i in range(self.start, x.shape[0]):
        y[i] = func(x[i]-self.start, self.a, self.b) 
      
     return y 


class TimeSeriesModel:
   def __init__(self, m):
      # m : number of the last data points
      # used to find the rate 
 
      self.rate = None 
      self.w = m 

   def fit(self, x, y):      
      n = x.shape[0]
      g = [y[i+1]/y[i] for i in range(n-self.w,n-1)]
      self.rate = np.mean (g)

   def predict(self, y_start,p):

      y = []
      #y = [y_start]
      for i in range (0, p):
         y_start *= self.rate 
         y.append(y_start)

      return np.array(y) 

