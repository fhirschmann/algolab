=====================
Clustering Algorithms
=====================

Station Clustering
------------------

The railway graph contains many nodes but certainly not all are important, the
subset of stations, however, is.

With station clustering we merge railway graph nodes with the nearest station if
they lie within a certain radius. This radius can be capped or it will extend to
half the distance to another station (i.e. a cluster endpoint).

This type of clustering can only work if there is already a collection
containing stations, the tool ``al_make_sg`` will construct such a collection.
Nodes in this collection have the following structure::

  {
  '_id': 123456789          # document id
  'loc': [42.23532, 23.542] # longitude, latitude
  'eva': '1000001'          # EVA number (string)
  }

Such a node has to have a corresponding node (i.e. same ID and location) in the
railway graph it is used with. The EVA is only used for diagnostic messages.

.. autofunction:: algolab.stations.cluster_stations
