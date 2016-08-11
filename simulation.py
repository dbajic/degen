import numpy as np
import itertools
import random
import sys
import networkx as nx
import math
from scipy import stats, misc

def degenerate(i,n,k):
    E = degenerate_wrapper(i,n,k,[0 for w in range(n)],set()) # Call wrapper function
    return E

def degenerate_wrapper(i,n,k,d,V):
    G = nx.Graph()
    for w in range(i,n+1):
        d[w-1] = restricted_binomial(n-w,min(n-w,k)) # Generate degree d_i for vertex v_i
        if (w == n): # Are we at the last vertex?
            V.add(n) # Add last vertex to vertex set
    for w in range(n,i-1,-1): # "Recurse" backwards
        combs = [None] * d[w-1] # Create list ahead of time to avoid list append overhead
        pool = list(V) # Pool of numbers to use for sample
        a = len(pool)
        for i in range(d[w-1]):
            index = int(random.random() * (a-i)) # Uniform sample between 0 and len(pool)-i
            combs[i] = pool[index]
            pool[index] = pool[a-i-1] # Faster than deleting (O(1) vs. O(n) operation)
        V.add(w) # Add vertex to vertex set
        G.add_node(w)
        for num in combs:
            G.add_edge(w,num)
    return G

def restricted_binomial(n,k):
    probs = []
    values = np.arange(k+1)
    sum_p = sum(misc.comb(n,i) for i in range(k+1)) # Save computation time by calculating the sum ahead of time
    for v in values:
        probs.append(misc.comb(n,v)/sum_p) # Create list of probabilities for each value
    rbin = stats.rv_discrete(name='rbin', values=(values,probs)) # Create probability density function
    sample = rbin.rvs() # Random sample from distribution
    return sample

def simulate(n,k,sims):
    suff_stats = []
    theta = [1,1] # We can make this not fixed later
    normConst = 0
    b = 0 # Max value for log-sum-exp trick
    for i in range(0,sims):
        G = degenerate(1,n,k)
        edges = len(G.edges())
        triangles = int(sum(nx.triangles(G).values())/3)
        if (edges + triangles) > b: # This just assumes theta = [1,1]
            b = edges + triangles
        suff_stats.append((edges, triangles))
    for s in suff_stats:
        normConst += math.exp((s[0]*theta[0]+s[1]*theta[1])-b)
    return b + math.log(normConst)

if __name__ == "__main__":
    print(simulate(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])))