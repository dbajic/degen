import numpy as np
import itertools
import random
import sys
import networkx as nx
import math
from scipy import stats, misc
from scipy.optimize import minimize
from joblib import Parallel, delayed

def restricted_binomial(n,k):
    probs = []
    values = np.arange(k+1)
    sum_p = sum(misc.comb(n,i) for i in range(k+1)) # Save computation time by calculating the sum ahead of time
    for v in values:
        probs.append(misc.comb(n,v)/sum_p) # Create list of probabilities for each value
    rbin = stats.rv_discrete(name='rbin', values=(values,probs)) # Create probability density function
    sample = rbin.rvs() # Random sample from distribution
    return sample

def degenerate(n,k):
    G = nx.Graph()
    d = [0 for a in range(n)]
    V = set()
    for w in range(1,n+1):
        d[w-1] = restricted_binomial(n-w,min(n-w,k)) # Generate degree d_i for vertex v_i
        if (w == n): # Are we at the last vertex?
            V.add(n) # Add last vertex to vertex set
    for w in range(n,0,-1): # "Recurse" backwards
        combs = [None] *  d[w-1] # Create list ahead of time to avoid list append overhead
        pool = list(V) # Pool of numbers to use for sample
        a = len(pool)
        for i in range(d[w-1]):
            index = int(random.random() * (a-i)) # Uniform sample between 0 and len(pool)-i
            combs[i] = pool[index]
            pool[index] = pool[a-i-1] # Faster than deleting (O(1) vs. O(n) operation)
        V.add(w) # Add vertex to vertex set
        for num in combs:
            G.add_edge(w,num)
    return (len(G.edges()), int(sum(nx.triangles(G).values())/3))

def getNormConst(theta,suff_stats):
    b = 0
    for stats in suff_stats:
        c = theta[0]*stats[0] + theta[1]*stats[1]
        if c > b:
            b = c
    return b + math.log(sum(math.exp((theta[0]*s[0]+theta[1]*s[1])-b) for s in suff_stats))

def f(theta,g,stats):
    return -(theta[0]*g[0] + theta[1]*g[1] - getNormConst(theta,stats))

def simulate(n,k,x):
    return degenerate(n,k)
	
if __name__ == "__main__":
	iters = range(int(sys.argv[3]))
	print("Sampling graphs...")
	graphs = Parallel(n_jobs=8, verbose=5)(delayed(simulate)(int(sys.argv[1]),int(sys.argv[2]),i) for i in iters)
	sampson = [41,18]
	theta0 = [0.5,0.6]
	print("Running model test...")
	res = minimize(f, theta0, args=(sampson,graphs,))
	print(res.x)
