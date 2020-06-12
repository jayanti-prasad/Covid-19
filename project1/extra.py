import argparse  
import sys
sys.path.append("../../pycov/")
from  PyCov19.epidemiology import Epidemology
import matplotlib.pyplot as plt  

if __name__ == "__main__":

   parser = argparse.ArgumentParser()
   parser.add_argument('-i','--input-file',help='Input csv file',\
      default='../data/covid-19-global.csv')
   parser.add_argument('-c','--country-name',help='Country name',\
      default='Italy')
   parser.add_argument('-o','--output-dir',help='Output dir',\
      default='results')

   args = parser.parse_args()

   E = Epidemology ('SEIR')
   #E = Epidemology ('SEIR','exp')

   R0 = 5.0 
   gamma = 1.0/14.0
   sigma = 1.0/7.0
   beta = R0 * gamma 
   print("gamma=",gamma,"sigma=",sigma,"beta=",beta)

   E.initilization (N=1000,E0=10,I0=10,R0=0)
   s = E.evolve (150,[gamma,sigma,beta])
   #s = E.evolve (size,[gamma,sigma, beta])

   plt.title('SEIR Model')
   plt.plot(s.t, s.y[0],c='b',label='Suceptible')
   plt.plot(s.t, s.y[1],c='r',label='Exposed')
   plt.plot(s.t, s.y[2],c='g',label='Infected')
   plt.plot(s.t, s.y[3],c='K',label='Recovered')
   plt.legend()
   plt.show()

