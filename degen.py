import numpy as np
import itertools
import random
import sys
from scipy import stats, misc

def degenerate(i,n,k):
    V,E = degenerate_wrapper(i,n,k,[0 for i in range(n)],set(),set()) # Call wrapper function
    return V,E

def degenerate_wrapper(i,n,k,d,V,E):
    if i == n: # Are we at the last vertex?
        V.add(n) # Add vertex to vertex set
    else:
        d[i-1] = restricted_binomial(n-i,min(n-i,k)) # Generate degree d_i for vertex v_i (!)
        degenerate_wrapper(i+1,n,k,d,V,E) # Recursively call function
        combs = []
        for r in itertools.combinations(V,d[i-1]): # Generate all subsets of degree d_i from V (!)
            combs.append(r)
        S = random.sample(combs,1)[0] # Uniformly sample one combination of edges
        E.add((i,S)) # Add corresponding edges to edge list
        V.add(i) # Add vertex to vertex list
    return V,E

def restricted_binomial(n,k):
    probs = []
    values = np.arange(k+1)
    sum_p = sum(misc.comb(n,i) for i in range(k+1)) # Save computation time by calculating the sum ahead of time
    for v in values:
        probs.append(misc.comb(n,v)/sum_p) # Create probability density function
    rbin = stats.rv_discrete(name='rbin', values=(values,probs))
    sample = rbin.rvs() # Random sample from distribution
    return sample
	
if __name__ == "__main__":
	V,E = degenerate(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
	G = [V,E]
	print(G)