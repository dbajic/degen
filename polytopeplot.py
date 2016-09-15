import simulation
import sys
import matplotlib.pyplot as plt
import numpy as np
from joblib import Parallel, delayed
from scipy.stats import gaussian_kde
	
if __name__ == "__main__":
	iters = range(int(sys.argv[3]))
	print("Sampling graphs...")
	graphs = Parallel(n_jobs=4, verbose=5)(delayed(simulation.simulate)(int(sys.argv[1]),int(sys.argv[2]),i) for i in iters)
	
	x = np.asarray([g[0] for g in graphs])
	y = np.asarray([g[1] for g in graphs])
	
	xy = np.vstack([x,y])
	z = gaussian_kde(xy)(xy)
	
	idx = z.argsort()
	x, y, z = x[idx], y[idx], z[idx]
	
	fig, ax = plt.subplots()
	ax.scatter(x, y, c=z, s=50, facecolors='none', edgecolor='', antialiased=True)
	plt.axis([0, 40, 0, 90])
	plt.xlabel('Edges')
	plt.ylabel('Triangles')
	fig.savefig('polytope_density.png', bbox_inches='tight')