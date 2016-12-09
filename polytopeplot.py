import matplotlib
matplotlib.use('Agg')
import simulation
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

if __name__ == "__main__":
	with open("samples.csv", 'r') as cw:
		reader = csv.reader(cw)
		graphs = list(reader)
	x = np.asarray([g[0] for g in graphs])
	y = np.asarray([g[1] for g in graphs])
	points = np.column_stack([x,y])
	fig, ax = plt.subplots()
	plt.hist2d(x,y,(50,50), cmin=1)
	plt.colorbar()

	hull = ConvexHull(points)
	for simplex in hull.simplices:
			plt.plot(points[simplex,0], points[simplex, 1], 'r')

	plt.xlabel('Edges')
	plt.ylabel('Triangles')

	plt.savefig('polytope.png', bbox_inches='tight')