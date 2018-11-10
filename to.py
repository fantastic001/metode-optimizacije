
import numpy as np 
import sys 
from collections import Counter

def get_input():
    n = int(input("Enter number of sources > "))
    m = int(input("Enter number of demands > "))

    sources = [float(input("Enter source for %dth source" % (i+1))) for i in range(n)]
    demands = [float(input("Enter demand for %dth sink" % (1+i))) for i in range(m)]
    C = np.zeros([n,m])
    for i in range(n):
        for j in range(m):
            C[i,j] = float(input("Enter cost for transport from %d to %d" % (i+1, j+1)))
    return sources, demands, C

def northwest(sources, demands, C):
    X = np.zeros([len(sources), len(demands)])
    i,j = (0,0) # northwest element
    while i < len(sources) and j < len(demands):
        if sources[i] < demands[j]:
            X[i,j] = sources[i]
            demands[j] -= sources[i]
            sources[i] = 0 
            i += 1
        else:
            X[i,j] = demands[j]
            sources[i] -= demands[j]
            demands[j] = 0
            j += 1
    return X 

def get_loop(X: np.array, i, j):
    r,c = X.shape
    n = r*c 
    paths = []
    for di, dj in [(0,1), (1,0), (-1, 0), (0, -1)]:
        paths.append([(i,j), (i+di, j+dj)])
    for k in range(n):
        new_paths = [] 
        for p in paths:
            #print(p)
            li, lj = p[-1]
            if li < 0 or li >= r or lj < 0 or lj >= c:
                continue
            lli, llj = p[-2]
            di = li - lli
            dj = lj - llj
            new_paths.append(p + [(li+di, lj + dj)])
            if X[li, lj] > 0:
                new_paths.append(p + [(li + dj, lj - di)])
                new_paths.append(p + [(li - dj, lj + di)])
        #print(k, " ", new_paths)
        paths = new_paths.copy()
        for p in new_paths:
            #print("Checking path: ", p[0], " -> ", p[-1])
            if p[0] == p[-1]:
                #print("Checking validity foor: ", p)
                if [(a,b) for a,b in p if a<0 or a >= len(sources) or 0 > b or b >= len(demands)] == []:
                    #print(" OK")
                    return p
    return None

def  uv_method(sources, demands, X, C):
    r,c = np.nonzero(X)
    if len(sources) + len(demands) - 1 != len(r):
        # degenerate case 
        # finding N - (n+m-1) epsilon variables
        diff = len(sources) + len(demands) - 1 - len(r)
        for k in range(diff):
            # add variable where we have found path and is not in dummmy
            for i in range(len(sources)):
                for j in range(len(demands)):
                    print("Loop found:")
                    print(get_loop(X,i,j))
                    if X[i,j] == 0 and get_loop(X, i,j) is not None:
                        X[i,j] = 0.00001 # assign very small value
    u = [np.nan for s in sources]
    v = [np.nan for d in demands]
    r,c = np.nonzero(X) # we have changed X maybe, we are updating list of nonzero values 
    u[0] = 0 
    #print(X)
    while [x for x in u if np.isnan(x)] + [x for x in v if np.isnan(x)] != []:
        for i,j in zip(list(r),list(c)):
            if np.isnan(u[i]):
                if not np.isnan(v[j]):
                    u[i] = C[i,j] - v[j]
            if np.isnan(v[j]):
                if not np.isnan(u[i]):
                    v[j] = C[i,j] - u[i]
            print(u + v)
    print("u: ", u)
    print("v: ", v)
    U = C*0
    V = C*0
    for i in range(len(sources)):
        U[i, :] = u[i] 
    for j in range(len(demands)):
        V[:, j] = v[j]
    print(U)
    print(V)
    print(C)
    P = U + V - C
    print("Peenalties:")
    print(P)
    return P, np.max(P) <= 0

def step(X, P):
    i,j = np.unravel_index(np.argmax(P), P.shape)
    print("Element with maximal penalty: ", i, j)
    rs, cs = np.where(X != 0) # get alloocated stuff
    path = get_loop(X, i,j)
    print("Loop: ", path)
    path = path[:-1]
    if path is None:
        print("Loop is not found")
        raise StopIteration()
    neg = path[1::2]
    pos = path[::2]
    q = min(X[i,j] for i,j in neg)
    print("Heuristic: %f" % q)
    if q == 0: 
        print("q is zero")
        raise StopIteration
    for i,j in neg:
        X[i,j] -= q
    for i,j in pos:
        X[i,j] += q
    return X 

sources, demands, C = get_input()
print("Northwest")
X = northwest(sources.copy(), demands.copy(), C.copy())
try:
    print("UV method")
    P, optimal = uv_method(sources.copy(), demands.copy(), X.copy(), C.copy())
    while not optimal:
        print("Step")
        X = step(X.copy(), P.copy())
        P, optimal = uv_method(sources.copy(), demands.copy(), X.copy(), C.copy())
        print(X)
    print("Solution: ")
    for row in X:
        for cell in row:
            sys.stdout.write("%f " % cell)
        print()
except StopIteration:
    print(X)
print("Total cost: %f" % (X*C).sum())