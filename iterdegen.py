import numpy as np
import itertools
import random
import sys
from scipy import stats, misc
from time import time

def degenerate(i,n,k):
    E = degenerate_wrapper(i,n,k,[0 for w in range(n)],set(),set()) # Call wrapper function
    return E

def degenerate_wrapper(i,n,k,d,V,E):
    for w in range(i,n+1):
        d[w-1] = restricted_binomial(n-w,min(n-w,k)) # Generate degree d_i for vertex v_i
        if (w == n): # Are we at the last vertex?
            V.add(n) # Add last vertex to vertex set
    for w in range(n,i-1,-1): # "Recurse" backwards
	# "Workaround" for generating all subsets of degree d_i from V
        selection = int(random.uniform(1, int(misc.comb(len(V),d[w-1])))) # Uniformly generate a random number between 1 and (|V| choose d_i) (!!!!!!)
        counter = 1
        for r in itertools.combinations(V,d[w-1]): # Loop until we generate the corresponding combination and append to edge set
            if counter == selection:
                E.add((w,r))
                V.add(w)
                break
            else:
                counter+=1
    return E

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
	start = time()
	E = degenerate(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
	end = time()
	print(E)
	print(end-start, "seconds")