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
        counter = 0
        temp = list(V)
        combs = []
		# Uniformly choose d_i distinct numbers from the current working vertex set and use as the combination
        while counter < d[w-1]:
            index = int(random.uniform(1, len(temp)))
            combs.append(temp[index-1])
            del temp[index-1]
            counter+=1
        E.add((w,tuple(num for num in combs)))
        V.add(w)
    return E

def restricted_binomial(n,k):
    probs = []
    values = np.arange(k+1)
    sum_p = sum(misc.comb(n,i) for i in range(k+1)) # Save computation time by calculating the sum ahead of time
    for v in values:
        probs.append(misc.comb(n,v)/sum_p)
    rbin = stats.rv_discrete(name='rbin', values=(values,probs)) # Create probability density function
    sample = rbin.rvs() # Random sample from distribution
    return sample
	
if __name__ == "__main__":
	graph = ""
	start = time()
	E = degenerate(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
	end = time()
	print(end-start, "seconds")
	# Create output file for the generated graph in an igraph-friendly format
	for t in E:
		A = list(zip(itertools.cycle([t[0]]),list(t[1])))
		for k,v in A:
			graph += str(k) + "," + str(v) + ","
	f = open("graph.txt", "w+")
	f.write(graph[0:-1])
	f.close()
	print("Graph generated: graph.txt")
	