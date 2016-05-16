import numpy as np
import itertools
import random
from scipy import stats, misc

def degenerate(i,n,k):
    V,E = degenerate_wrapper(i,n,k,[0 for i in range(n)],set(),set())
    return V,E

def degenerate_wrapper(i,n,k,d,V,E):
    if i == n: # Are we at the last node?
        V.add(n)
    else:
        d[i-1] = restricted_binomial(n-i,min(n-i,k)) # Generate degree d_i for vertex v_i
        degenerate_wrapper(i+1,n,k,d,V,E)
        combs = []
        for r in itertools.combinations(V,d[i-1]): # Generate all subsets of degree d_i from V
            combs.append(r)
        S = random.sample(combs,1)[0] # Uniformly sample one element from combinations
        E.add((i,S))
        V.add(i)
    return V,E

def restricted_binomial(n,k):
    probs = []
    values = np.arange(k+1)
    sum_p = sum(misc.comb(n,i) for i in range(k+1))
    for v in values:
        probs.append(misc.comb(n,v)/sum_p)
    rbin = stats.rv_discrete(name='rbin', values=(values,probs)) 
    sample = rbin.rvs()
    return sample
	
if __name__ == "__main__":
	V,E = degenerate(1,100,4)
	G = [V, E]
	print(G)