import numpy as np
import itertools
import random
import sys

def degenerate(n,m,k):
	V = [i for i in range(0,n+1)] # Vertex set
	E = [] # Edge set
	d = [0 for i in range(0,n+1)] # Degrees of each vertex
	C = [i for i in range(1,n)] # Set of working vertices
    
	for i in range(1,m+1):
		vertex = np.random.choice(C) # Uniformly choose a vertex from working set
		d[vertex]+=1 # Increase degree of chosen vertex
		if d[vertex] == min(n-vertex,k): # Does the degree of the chosen vertex exceed what's "allowed"
			C.remove(vertex) # If yes, remove it from working set
	# Unformly choose vertices to connect edges
	for i in range(n-1,0,-1):
		counter = 0
		combs = []
		temp = [j for j in range(i+1,n+1)]
		while counter < d[i]:
			index = int(random.uniform(1,len(temp)+1))
			combs.append(temp[index-1])
			del temp[index-1]
			counter+=1
		E.append((i,tuple(num for num in combs)))
	return E

def makegraphs(num,n,m,k):
	i = -1 if num == 0 else 0 # Check to see if we want only the graph or files for graphs
	while i < num:
		graph = ""
		E = degenerate(n,m,k)
		# Create output file(s) for the generated graph in an igraph-friendly format
		for t in E:
			A = list(zip(itertools.cycle([t[0]]),list(t[1])))
			for k,v in A:
				graph += str(k) + "," + str(v) + ","
		if num == 0: # Don't want a file, just give the graph
			print(graph[0:-1])
			return
		else:
			f = open("graph" + str(i) + ".txt", "w+")
			f.write(graph[0:-1])
			f.close()
			i+=1
	
	return

if __name__ == "__main__":
	files = int(sys.argv[4])
	if int(files) >= 1000:
		check = input("Are you sure you want to generate that many files? (y/n) ")
		if check == "n":
			sys.exit()
		elif check == "y":
			makegraphs(files,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
	else:
		makegraphs(files,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))