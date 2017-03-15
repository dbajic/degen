*k*-degenerate Graph Generator(s)
=============

These are a series of Python generators used for uniform *k*-degenerate graph generation dependent on specific parameters.

0. Parameters that can be modified include number of vertices, number of edges, maximum degeneracy, and number of graphs generated.
0. Polytopes of sampled graphs can be plotted.

Usage
-----

To run a simulation:

```python simulation.py [vertices] [degeneracy] [samples] [[models]]```

```python simulation.py [vertices] [edges] [degeneracy] [samples]``` ** Currently under construction **

Currently supported models: ```edge, triangle, degseq, 2-star```

To plot the estimated DERGM polytope:

```python polytopeplot.py``` ** Works with CSV Edge-Triangle model at the moment **

Monte Carlo MLE and Entropy plots can be found running ```dergminfo.R```

** Example: **

```python simulation.py 3 2 10 edge triangle 2-star degseq```
```
Models: ['Edge', 'Triangle', 'Degree Sequence', '2-star']
0       0       0,0,0   0
3       1       2,2,2   3
1       0       0,1,1   0
2       0       1,2,1   1
2       0       2,1,1   1
1       0       0,1,1   0
3       1       2,2,2   3
2       0       2,1,1   1
2       0       2,1,1   1
2       0       1,1,2   1
```

Contributing
------------

The basis for this code comes from the work of Bauer, Krug, and Wagner in [Enumerating and Generating Labeled k-degenerate Graphs](http://epubs.siam.org/doi/abs/10.1137/1.9781611973006.12)

Results from this code can be found in [DERGMs: Degeneracy-restricted exponential random graph models] (Karwa, Petrovic, Bajic)