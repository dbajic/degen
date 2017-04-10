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
from collections import defaultdict

def restricted_binomial(n,k):
        probs = []
        values = np.arange(k+1)
        sum_p = sum(misc.comb(n,i) for i in range(k+1)) # Save computation time by calculating the sum ahead of time
        for v in values:
                        probs.append(misc.comb(n,v)/sum_p) # Create list of probabilities for each value
        rbin = stats.rv_discrete(name='rbin', values=(values,probs)) # Create probability density function
        sample = rbin.rvs() # Random sample from distribution
        return sample

def degenerate(n,k,star=1):
        G = nx.Graph()
        d = [0 for a in range(n)]
        V = set()
        model = []
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
        model.append(str(len(G.edges()))) # Add edge model
        model.append(str(int(sum(nx.triangles(G).values())/3))) # Add triangle model
        degseq = defaultdict(lambda: 0) # Default to if a degree is not listed by NetworkX then the degree of that node is 0
        if (G.degree() != {}): # Sometimes all of the degrees are 0 :(
                for node,degree in G.degree(range(1,n+1)).items():
                        degseq[node] = degree
        sequence = str(degseq[1])
        for i in range(2,n+1):
                sequence += "," + str(degseq[i]) # CSV for each node degree
        model.append(sequence)
        stars = int(sum([misc.comb(x,star) for x in G.degree().values()])) # How many total 2-stars are in the graph
        model.append(str(stars))
        return model # Give all possible models for user to choose


def edge_degenerate(n,m,k): # Not used at the moment, will be updated
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

def simulate(n,k,x,stars):
        return degenerate(n,k,stars)

def esimulate(n,m,k,x):
        return edge_degenerate(n,m,k)

# This writes output to console now instead of to CSV
# The idea is that cluster takes output from stdout to put into file, so it's redundant to do it a 2nd time
if __name__ == "__main__":
        if (len(sys.argv)) >= 5:
                        iters = range(0, int(sys.argv[3]))
                        models = [] # Which models are we using
                        if ('edge' in sys.argv):
                                models.append("Edge")
                        if ('triangle' in sys.argv):
                                models.append("Triangle")
                        if ('degseq' in sys.argv):
                                models.append("Degree Sequence")
                        if ('star' in sys.argv):
                                idx = sys.argv.index("star") + 1
                                numstars = int(sys.argv[idx])
                                models.append(str(numstars) + "-star")
                        graphs = Parallel(n_jobs=8)(delayed(simulate)(int(sys.argv[1]),int(sys.argv[2]),i,numstars) for i in iters)
                        print("Models: " + str(models))
                        for g in graphs:
                                model = ""
                                if ('edge' in sys.argv): #Edge model
                                        model += g[0] + "\t"
                                if ('triangle' in sys.argv): #Triangle model
                                        model += g[1] + "\t"
                                if ('degseq' in sys.argv): #Degree Sequence model
                                        model += g[2] + "\t"
                                if ('star' in sys.argv): #k-star model
                                        model += g[3] + "\t"
                                print(model)
        #elif (len(sys.argv)) == 6: # Not fully implemented for different models right now
                        #iters = range(int(sys.argv[4]))
                        #graphs = Parallel(n_jobs=4, verbose=5)(delayed(esimulate)(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),i) for i in iters)
