import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from PyCov19.beta_models import  exp, tanh

font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['axes.linewidth'] = 2.0


if __name__ == "__main__":

   n = 500
   t = np.linspace(1.0,n,n)

   params = [{'beta_0': 0.24, 'alpha': 0.4, 'mu': 0.01, 'tl': 50.0}]
   params.append({'beta_0': 0.24, 'alpha': 0.5, 'mu': 0.01, 'tl': 50.0})
   params.append({'beta_0': 0.24, 'alpha': 0.4, 'mu': 0.04, 'tl': 50.0})
   params.append({'beta_0': 0.24, 'alpha': 0.5, 'mu': 0.04, 'tl': 50.0})

   fig = plt.figure (figsize=(12,9)) 
   ax = fig.add_subplot(111)
   ax.set_xlabel('t')
   ax.set_ylabel('$\\beta(t)$')

   for p in params:
      beta = [ exp (x, **p) for x in t]
      label = '$\\alpha$='+str(p['alpha'])+", $\\mu=$" + str(p['mu'])

      ax.plot(t, beta,label=label)
 
   plt.legend()
   plt.savefig("plots/beta_exp.pdf")
   #plt.show()


