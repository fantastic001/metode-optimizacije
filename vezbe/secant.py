
import matplotlib.pyplot as plt 

def secant(df, a, b, epsilon):
    while abs(a-b) > epsilon:
        print(a,b)
        (a,b) = (a - df(a)*(b-a) / (df(b) - df(a)), a)
    return a


import numpy as np

if __name__ == "__main__":
    f = lambda x: x**3 + x**2 + 5*x + 3 
    x = np.arange(-500, 500)
    plt.plot(x, np.vectorize(f)(x))
    plt.show()
    print(secant(lambda x: 3*x**2 + 2*x + 5, -561561, 546456, 0.0001))