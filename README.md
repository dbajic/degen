*k*-degenerate Graph Generator(s)
=============

These are a series of Python generators used for uniform *k*-degenerate graph generation dependent on specific parameters.

0. Parameters that can be modified include number of vertices, number of edges, maximum degeneracy, number of graphs generated, and different model specifications.
0. Polytopes of sampled graphs can be plotted.

Usage
-----

To run a simulation:

```python simulation.py [vertices] [degeneracy] [samples] [[models]]```

```python simulation.py [vertices] [edges] [degeneracy] [samples]``` **Currently under construction**

Currently supported models: ```edge, triangle, degseq, star [num] (k-stars)```

To plot the estimated DERGM polytope:

```python polytopeplot.py``` **Works with CSV Edge-Triangle model at the moment**

Monte Carlo MLE and Entropy plots can be found running ```dergminfo.R```

**Example:**

```python simulation.py 10 6 10 edge triangle star 3 degseq```
```
Models: ['Edge', 'Triangle', 'Degree Sequence', '3-star']
18      4       2,4,5,4,4,3,3,3,5,3     36
15      3       3,4,3,2,4,1,2,3,6,2     31
19      9       2,4,4,4,3,2,6,3,3,7     70
21      10      3,7,6,3,3,5,4,5,2,4     86
25      18      6,4,5,6,5,6,2,4,6,6     128
24      16      6,3,6,4,5,5,4,3,7,5     115
17      4       3,3,3,4,2,6,3,2,3,5     39
22      14      4,2,4,6,6,5,5,4,2,6     92
23      14      5,4,6,6,2,3,4,7,4,5     108
25      19      4,6,6,5,5,4,7,7,3,3     140
```

Contributing
------------

The basis for this code comes from the work of Bauer, Krug, and Wagner in [Enumerating and Generating Labeled k-degenerate Graphs](http://epubs.siam.org/doi/abs/10.1137/1.9781611973006.12)

Results from this code can be found in [DERGMs: Degeneracy-restricted exponential random graph models](https://arxiv.org/abs/1612.03054) (Karwa, Petrovic, Bajic)