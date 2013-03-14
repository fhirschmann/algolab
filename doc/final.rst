.. _final_report:

====================
Final Report (Draft)
====================

This document describes how the complete graphs for all zoom levels
were constructed and how well our algorithms did. It is assumed
that you have correctly :ref:`setup` your environment.

Introduction
============

We used a combination of multiple algorithms, namely the Ramer-Douglas-Peucker Algorithm
(:func:`~algolab.simplify.rdp`), an angle-based Line Combination Algorithm
(:func:`~algolab.combine.anglecombine`), and a Clustering Algorithm
(:func:`~algolab.stations.cluster_stations`).

Where appropriate, our algorithms operate on a spherical mercator projections adapted
to the region of interest (see :func:`~algolab.util.ll2xy`).
This also means that the parameter given to :func:`~algolab.simplify.rdp` is in meters.

Result Reproduction
===================

Step 1: OSM Import
------------------

This step imports the railway graph from the osm data::

    java -jar osm_railway_graph_import.jar germany.osm 127.0.0.1 27017


Step 2: Our Algorithms
----------------------

This is the step were our project kicks in. It works on the railway
graph and produces a generalized railway graph for each zoom level.

The main entry point for producing generalized railway graphs is
``al_tool``:

  .. program-output:: al_tool --help

It has three subcommands: ``al_tool prepare``, ``al_tool stations`` and
``al_tool filter``. Each subcommand has its own ``--help`` option.

.. note::

   The scripts in ``bin/`` assume that the ``algolab`` code tree is in its
   parent directory. If you want to change the provided directory structure add the
   directory that contains ``algolab`` to the ``PYTHONPATH`` or place ``algolab``
   into a directory that is already in it.

The zoom levels indicate what collection will be produced. For example, running
``al_tool filter 14`` will produce the collection ``railway_graph_14``. Multiple
zoom levels can be specified (e.g. ``al_tool filter 16 15 14``), but keep in
mind that a zoom level usually depends on its predecessor level. Additionally,
you can create all zoomlevels using ``al_tool filter --all-zoomlevels``.

In the following sections, the images on the left-hand side represent
the Frankfurt Main Station and the image on the right-hand side represent
the Rhine-Main-Area (Frankfurt, Mainz, Darmstadt).

After importing OSM data you need to execute these steps:

  #. ``al_tool prepare``
  #. ``al_tool stations``
  #. ``al_tool filter``

Of course each with appropriate arguments. Furthermore, ``al_tool stations``
generates a ``ZoomLevelStations.txt`` (you can influence where this is written
using the ``-f`` option).

.. note::

    Zoom level 17 is no zoom level that is used by Google Maps. Instead, this
    zoom level is our general cleaning stat that does the following:

    - Removed nodes that have no neighbors

    - Remove duplicates (nodes with the same ``loc`` attribute)

    - Recalculate all distances (great-circle distance)

    This step can be executed by running::

        al_tool prepare

.. all images were produced using
   al_visualize_rg -s doc/img/step-x.png -t "Zoom Level x" \
                   --dpi 75 -c railway_graph_x

Algorithm Combination Summary
=============================

The following table illustrates how our algorithms were combined:

+------------+---------------------------------------------------------------------------------------------+
| Zoom level | Algorithms used                                                                             |
+============+=============================================================================================+
|         17 | :func:`~algolab.db.dedup`, :func:`~algolab.db.delonelynize`                                 |
+------------+---------------------------------------------------------------------------------------------+
|         16 | :func:`~algolab.simplify.rdp` with ε=1.3m                                                   |
+------------+---------------------------------------------------------------------------------------------+
|         15 | :func:`~algolab.simplify.rdp` with ε=2.6m                                                   |
+------------+---------------------------------------------------------------------------------------------+
|         14 | :func:`~algolab.simplify.rdp` with ε=3.9m                                                   |
+------------+---------------------------------------------------------------------------------------------+
|         13 | :func:`~algolab.simplify.rdp` with ε=5.2m                                                   |
+------------+---------------------------------------------------------------------------------------------+
|         12 | :func:`~algolab.simplify.rdp` with ε=6.5m                                                   |
+------------+---------------------------------------------------------------------------------------------+
|         11 | :func:`~algolab.stations.cluster_stations`, :func:`~algolab.simplify.rdp` with ε=6.5m       |
+------------+---------------------------------------------------------------------------------------------+
|         10 | :func:`~algolab.combine.anglecombine` with ε=10°, :func:`~algolab.simplify.rdp` with ε=6.5m |
+------------+---------------------------------------------------------------------------------------------+
|          9 | :func:`~algolab.simplify.rdp` with ε=10m                                                    |
+------------+---------------------------------------------------------------------------------------------+
|          8 | :func:`~algolab.simplify.rdp` with ε=20m                                                    |
+------------+---------------------------------------------------------------------------------------------+

Area Results
============

Germany
-------
This section is devoted to the entire map of Germany.

Log
^^^

Feeding our software the complete data set yields the following result::

    [2013-03-14 08:27:49,373] --------------------------------------------------
    [2013-03-14 08:27:49,373] => Starting step 'Overall process'
    [2013-03-14 08:27:49,609] --------------------------------------------------
    [2013-03-14 08:27:49,609] => Starting step 'Zoom Level 16'
    [2013-03-14 08:27:49,783] --------------------------------------------------
    [2013-03-14 08:27:49,783] => Starting step 'Applying RDP with eps=1.600000'
    Applying rdp to segment 146377 of 135154 (estimated) (108.30%)
    [2013-03-14 08:54:07,269] Reduced to 530949 nodes from 870102 nodes. Change: -339153 (-38.979%)
    [2013-03-14 08:54:07,269] <= Step 'Applying RDP with eps=1.600000' finished (took 0:26:17.486040).
    [2013-03-14 08:54:07,269] <= Step 'Zoom Level 16' finished (took 0:26:17.660210).
    [2013-03-14 08:54:07,270] --------------------------------------------------
    [2013-03-14 08:54:07,270] => Starting step 'Zoom Level 15'
    [2013-03-14 08:54:07,340] --------------------------------------------------
    [2013-03-14 08:54:07,340] => Starting step 'Applying RDP with eps=3.200000'
    Applying rdp to segment 146299 of 135089 (estimated) (108.30%)
    [2013-03-14 09:18:24,391] Reduced to 415546 nodes from 530949 nodes. Change: -115403 (-21.735%)
    [2013-03-14 09:18:24,391] <= Step 'Applying RDP with eps=3.200000' finished (took 0:24:17.050890).
    [2013-03-14 09:18:24,391] <= Step 'Zoom Level 15' finished (took 0:24:17.121100).
    [2013-03-14 09:18:24,391] --------------------------------------------------
    [2013-03-14 09:18:24,391] => Starting step 'Zoom Level 14'
    [2013-03-14 09:18:24,489] --------------------------------------------------
    [2013-03-14 09:18:24,489] => Starting step 'Applying RDP with eps=4.800000'
    Applying rdp to segment 145968 of 134745 (estimated) (108.33%)
    [2013-03-14 09:41:36,956] Reduced to 353198 nodes from 415546 nodes. Change: -62348 (-15.004%)
    [2013-03-14 09:41:36,956] <= Step 'Applying RDP with eps=4.800000' finished (took 0:23:12.466771).
    [2013-03-14 09:41:36,956] <= Step 'Zoom Level 14' finished (took 0:23:12.564977).
    [2013-03-14 09:41:36,956] --------------------------------------------------
    [2013-03-14 09:41:36,956] => Starting step 'Zoom Level 13'
    [2013-03-14 09:41:37,051] --------------------------------------------------
    [2013-03-14 09:41:37,051] => Starting step 'Applying RDP with eps=6.400000'
    Applying rdp to segment 145496 of 134256 (estimated) (108.37%)
    [2013-03-14 10:04:17,655] Reduced to 314893 nodes from 353198 nodes. Change: -38305 (-10.845%)
    [2013-03-14 10:04:17,655] <= Step 'Applying RDP with eps=6.400000' finished (took 0:22:40.604271).
    [2013-03-14 10:04:17,655] <= Step 'Zoom Level 13' finished (took 0:22:40.699050).
    [2013-03-14 10:04:17,655] --------------------------------------------------
    [2013-03-14 10:04:17,655] => Starting step 'Zoom Level 12'
    [2013-03-14 10:04:17,730] --------------------------------------------------
    [2013-03-14 10:04:17,731] => Starting step 'Applying RDP with eps=8.000000'
    Applying rdp to segment 144823 of 133656 (estimated) (108.36%)
    [2013-03-14 10:26:27,475] Reduced to 288767 nodes from 314893 nodes. Change: -26126 (-8.297%)
    [2013-03-14 10:26:27,475] <= Step 'Applying RDP with eps=8.000000' finished (took 0:22:09.744512).
    [2013-03-14 10:26:27,475] <= Step 'Zoom Level 12' finished (took 0:22:09.819714).
    [2013-03-14 10:26:27,475] --------------------------------------------------
    [2013-03-14 10:26:27,475] => Starting step 'Zoom Level 11'
    Clustering Station [2013-03-14 10:31:37,433] Railway graph does not contain ID 1663109383, will ignore it
    Clustering Station 16836 of 16836 (100.00%)
    [2013-03-14 10:33:13,896] Reduced to 148305 nodes from 288767 nodes. Change: -140462 (-48.642%)
    [2013-03-14 10:33:13,896] --------------------------------------------------
    [2013-03-14 10:33:13,896] => Starting step 'Applying RDP with eps=6.000000'
    Applying rdp to segment 84934 of 69618 (estimated) (122.00%)
    [2013-03-14 10:42:43,922] Reduced to 146189 nodes from 148305 nodes. Change: -2116 (-1.427%)
    [2013-03-14 10:42:43,922] <= Step 'Applying RDP with eps=6.000000' finished (took 0:09:30.025777).
    [2013-03-14 10:42:43,922] <= Step 'Zoom Level 11' finished (took 0:16:16.446759).
    [2013-03-14 10:42:43,922] --------------------------------------------------
    [2013-03-14 10:42:43,922] => Starting step 'Zoom Level 10'
    [2013-03-14 10:42:44,046] --------------------------------------------------
    [2013-03-14 10:42:44,047] => Starting step 'Applying Anglecombine with eps=10.000000'
    Intersections left: 0()00
    [2013-03-14 10:49:59,152] Reduced to 92029 nodes from 146189 nodes. Change: -54160 (-37.048%)
    [2013-03-14 10:49:59,152] <= Step 'Applying Anglecombine with eps=10.000000' finished (took 0:07:15.105290).
    [2013-03-14 10:49:59,152] --------------------------------------------------
    [2013-03-14 10:49:59,152] => Starting step 'Applying RDP with eps=6.000000'
    Applying rdp to segment 41023 of 29927 (estimated) (137.08%)
    [2013-03-14 10:53:15,207] Reduced to 88478 nodes from 92029 nodes. Change: -3551 (-3.859%)
    [2013-03-14 10:53:15,207] <= Step 'Applying RDP with eps=6.000000' finished (took 0:03:16.054443).
    [2013-03-14 10:53:15,207] <= Step 'Zoom Level 10' finished (took 0:10:31.284804).
    [2013-03-14 10:53:15,207] --------------------------------------------------
    [2013-03-14 10:53:15,207] => Starting step 'Zoom Level 9'
    [2013-03-14 10:53:15,258] --------------------------------------------------
    [2013-03-14 10:53:15,259] => Starting step 'Applying RDP with eps=10.000000'
    Applying rdp to segment 40979 of 29978 (estimated) (136.70%)
    [2013-03-14 10:56:23,713] Reduced to 82628 nodes from 88478 nodes. Change: -5850 (-6.612%)
    [2013-03-14 10:56:23,713] <= Step 'Applying RDP with eps=10.000000' finished (took 0:03:08.454232).
    [2013-03-14 10:56:23,713] <= Step 'Zoom Level 9' finished (took 0:03:08.505563).
    [2013-03-14 10:56:23,713] --------------------------------------------------
    [2013-03-14 10:56:23,713] => Starting step 'Zoom Level 8'
    [2013-03-14 10:56:23,747] --------------------------------------------------
    [2013-03-14 10:56:23,747] => Starting step 'Applying RDP with eps=20.000000'
    Applying rdp to segment 40896 of 29927 (estimated) (136.65%)
    [2013-03-14 10:59:20,114] Reduced to 68220 nodes from 82628 nodes. Change: -14408 (-17.437%)
    [2013-03-14 10:59:20,114] <= Step 'Applying RDP with eps=20.000000' finished (took 0:02:56.367118).
    [2013-03-14 10:59:20,114] <= Step 'Zoom Level 8' finished (took 0:02:56.401245).
    [2013-03-14 10:59:20,116] <= Step 'Overall process' finished (took 2:31:30.743248).

Summary
^^^^^^^

+------------+------------+----------------+
| Zoom level | # of nodes | Time spent     |
+============+============+================+
|            |     870136 |                |
+------------+------------+----------------+
|         17 |     870102 | 0:26:17.660210 |
+------------+------------+----------------+
|         16 |     530949 | 0:24:17.050890 |
+------------+------------+----------------+
|         15 |     415546 | 0:23:12.564977 |
+------------+------------+----------------+
|         14 |     353198 | 0:23:12.564977 |
+------------+------------+----------------+
|         13 |     314893 | 0:22:40.699050 |
+------------+------------+----------------+
|         12 |     288767 | 0:22:09.819714 |
+------------+------------+----------------+
|         11 |     146189 | 0:16:16.446759 |
+------------+------------+----------------+
|         10 |      88478 | 0:10:31.284804 |
+------------+------------+----------------+
|          9 |      82628 | 0:03:08.505563 |
+------------+------------+----------------+
|          8 |      68220 | 0:02:56.401245 |
+------------+------------+----------------+
| Total      |            | 2:31:30.743248 |
+------------+------------+----------------+

Frankfurt Metropolitan Area
---------------------------

Log
^^^

Visualization
^^^^^^^^^^^^^

.. image:: img/ffm/rg-zl-17.png
.. image:: img/ffm/rg-zl-16.png
.. image:: img/ffm/rg-zl-15.png
.. image:: img/ffm/rg-zl-14.png
.. image:: img/ffm/rg-zl-13.png
.. image:: img/ffm/rg-zl-12.png
.. image:: img/ffm/rg-zl-11.png
.. image:: img/ffm/rg-zl-10.png
.. image:: img/ffm/rg-zl-9.png
.. image:: img/ffm/rg-zl-8.png

Summary
^^^^^^^
