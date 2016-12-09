*k*-degenerate Graph Generator(s)
=============

These are a series of Python generators used for uniform *k*-degenerate graph generation dependent on specific parameters.

0. Parameters that can be modified include number of vertices, number of edges, maximum degeneracy, and number of graphs generated.
0. Polytopes of samples graphs can be plotted.

Usage
-----

To run a simulation:

```python simulation.py [vertices] [degeneracy] [samples]```

```python simulation.py [vertices] [edges] [degeneracy] [samples]```

To plot the estimated DERGM polytope:

```python polytopeplot.py```

Calculations for Monte Carlo MLE and Entropy plots can be found running ```dergminfo.R```

Contributing
------------

The basis for this code comes from the work of Bauer, Krug, and Wagner in [Enumerating and Generating Labeled k-degenerate Graphs](http://epubs.siam.org/doi/abs/10.1137/1.9781611973006.12)