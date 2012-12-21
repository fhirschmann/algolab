==========================
Line Combination Algorithm
==========================

Imported train tracks often run in parallel. It is however
not even possible to distinguish between two tracks at a
mid-level zoom levels. Thus, we propose a simple algorithm
that takes care of this matter and combines several parallel
train tracks.

Angle-based Combination
-----------------------

The angle-based combination algorithm works as follows::

    for each intersection:
        if the angle between two neighbors n₁ and n₂ is < ε:
            (if the length of the line segment n₁ n₂ is <  δ:)
                replace n₁ and n₂ with a node located at the
                midpoint of the line segment


.. autofunction:: algolab.combine.anglecombine

The following images illustrate the initial problem:

.. plot::

    from algolab.plot import plot_datasets
    plot_datasets([12, 13, 14, 15], "Initial Situation")

Applying the algorithm with ε = 30 gives:

.. plot::

    from algolab.plot import plot_rg
    from algolab.test import rg_from_datasets
    from algolab.combine import anglecombine
    rg = rg_from_datasets([12, 13, 14, 15])
    anglecombine(rg, 30)
    plot_rg(rg, "After anglecombine with epsilon=30")
