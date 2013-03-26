Discarded Approaches
====================

Angle-Based-Reduction
---------------------

The approach described in :ref:`simp_angle` was not used because the
:ref:`simp_rdp` was superior under nearly all circumstances.

However, the algorithm could have been improved by first computing and then
sorting all angles in a segment instead of just checking if an angle
is within a certain threshold locally.

Filtering of railway graph nodes based on valuation
---------------------------------------------------

We planned to value railway graph nodes and omit nodes which did not exceed a
threshold appropriate for a given zoomlevel.

We did not pursued this approach as it was difficult to find suitable metrics to
value the nodes. This was easy for certain classes of nodes, e.g. nodes with a
nearby station or endpoints, but for most nodes we could not find a method to
valuate them.
