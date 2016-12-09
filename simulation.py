import numpy as np
import itertools
import random
import sys
import networkx as nx
import math
import csv
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
	
def edge_degenerate(n,m,k):
	G = nx.Graph()
	V = [range(0,n+1)]
	d = [0 for i in range(0,n)]
	C = [i for i in range(1,n)]
	
	for i in range(1,m+1):
		vertex = C[int(random.uniform(0,len(C)))]
		d[vertex-1] += 1
		if d[vertex-1] == min(n-vertex, k):
			C.remove(vertex)
	for i in range(n-1,0,-1):
		combs = [None] * d[i-1]
		pool = [j for j in range(i+1,n+1)]
		a = len(pool)
		for j in range(d[i-1]):
			index = int(random.random() * (a-j))
			combs[j] = pool[index]
			pool[index] = pool[a-j-1]
		for num in combs:
			G.add_edge(i,num)
	return (len(G.edges()), int(sum(nx.triangles(G).values())/3), True)

def simulate(n,k,x):
	return degenerate(n,k)

def esimulate(n,m,k,x):
	return edge_degenerate(n,m,k)
	
if __name__ == "__main__":
	print("Sampling graphs...")
	if (len(sys.argv)) == 4:
		iters = range(int(sys.argv[3]))
		graphs = Parallel(n_jobs=4, verbose=5)(delayed(simulate)(int(sys.argv[1]),int(sys.argv[2]),i) for i in iters)
	elif (len(sys.argv)) == 5:
		iters = range(int(sys.argv[4]))
		graphs = Parallel(n_jobs=4, verbose=5)(delayed(esimulate)(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),i) for i in iters)
	with open('samples.csv', 'w', newline='') as cfile:
		cw = csv.writer(cfile, delimiter=',')
		for g in graphs:
			for edge in g.edges():
				cw.writerow([edge[0], edge[1]])