.. _final_report:

============
Final Report
============

This document describes how the complete graphs for all zoom levels
was constructed and how well our algorithms did.

Step 1: OSM Import
==================

This step imports the railway graph from the osm data:

    java -jar osm_railway_graph_import.jar germany.osm 127.0.0.1 27017

Step 2: Our Algorithms
======================

This is the step were our project kicks in. It works on the railway
graph and produces a generalized railway graph for each zoom level.

The main entry point for producing generalized railway graphs is
`al_filter`:

  .. program-output:: al_filter --help

The zoom levels indicate what collection will be produced. For example,
running `al_filter 14` will produce the collection `railway_graph_14`.

In the following sections, the images on the left-hand side represent
the Frankfurt Main Station and the image on the right-hand side represent
Germany.

Zoom level 30
-------------

This is no zoom level that is used by google maps. Instead, this
is our general cleaning step that does the following:

- Remove nodes that have no neighbors

- Remove duplicates (nodes with the same `loc` attribute)

- Recalculate all distances (great-circle distance)

This step is executed by running::

    al_filter 30

.. all images were produced using
   al_visualize_rg -s doc/img/step-x.png -t "Zoom Level x" \
                   --dpi 75 -c railway_graph_x

Initial Situation
-----------------

.. image:: img/step-initial.png


Zoom level 16
-------------

.. image:: img/step-16.png

Zoom level 15
-------------

Zoom level 14
-------------

Zoom level 13
-------------

Zoom level 12
-------------

Zoom level 11
-------------

Zoom level 10
-------------

Zoom level 9
------------

Zoom level 8
------------

Node Quantity Results
---------------------

The following table illustrates the application of our algorithms
and the result thereof.

+------------+------------------------------+------------------+--------------------+
| Zoom level | Algorithms used              | #nodes (Germany) | #nodes (Frankfurt) |
+============+==============================+==================+====================+
|            |                              |                  | 7710               |
+------------+------------------------------+------------------+--------------------+
| 30         | dedup, delonelynize          |                  | 7710               |
+------------+------------------------------+------------------+--------------------+
| 16         | rdp(ε=1.5m)                  |                  | 3896               |
+------------+------------------------------+------------------+--------------------+
