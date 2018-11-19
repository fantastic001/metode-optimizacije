
def newton(df, ddf, x0, epsilon):
    x = x0 - df(x0) / ddf(x0)
    while abs(x - x0) > epsilon:
        (x0, x) = x, x0 - df(x0) / ddf(x0)
    return x 

if __name__ == "__main__":
    f = lambda x: x**2 + 5*x + 3 
    print(newton(lambda x: 2*x + 5, lambda x: 2, -561561, 0.0001))