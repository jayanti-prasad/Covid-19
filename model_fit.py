import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit


def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


def func(x, a, b, c):
   return a * np.exp(-b * x) + c

if __name__ == "__main__":
    xdata = np.linspace(0, 4, 50)
    y = func(xdata, 2.5, 1.3, 0.5)

    np.random.seed(1729)
    y_noise = 0.2 * np.random.normal(size=xdata.size)
    ydata = y + y_noise

    plt.plot(xdata, ydata, 'b-', label='data')


    popt, pcov = curve_fit(func, xdata, ydata)

    print("params:",popt[0],popt[1],popt[1])

    plt.plot(xdata, func(xdata, *popt), 'r-',\
      label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.show()
