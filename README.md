*k*-degenerate Graph Generator(s)
=============

These are a series of Python generators used for uniform *k*-degenerate graph generation dependent on specific parameters.

0. Parameters that can be modified include number of vertices, number of edges, maximum degeneracy, and number of graphs generated.
0. These generators can be connected to CRAN's [igraph](https://github.com/igraph/igraph) package. (Outdated)

Usage
-----

For uniform graph generation with vertex and degeneracy parameters:

```python degen.py [vertices] [degeneracy] [files]```

```python nudegen.py [vertices] [edges] [degeneracy] [files]```

To run a simulation:

```python simulation.py [vertices] [degeneracy] [samples]```

To plot polytopes:

```python polytopeplot.py [vertices] [degeneracy] [samples]```

Contributing
------------

The basis for this code comes from the work of Bauer, Krug, and Wagner in [Enumerating and Generating Labeled k-degenerate Graphs](http://epubs.siam.org/doi/abs/10.1137/1.9781611973006.12)