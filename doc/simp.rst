=============================
Line Simplifaction Algorithms
=============================

.. _simp_angle:

Angle-based Reduction
----------------------

.. autofunction:: algolab.simplify.anglereduce

Examples: Given the following initial situation:

.. plot::

    from algolab.plot import plot_algo
    plot_algo(lambda x: x, 0, "Initial Situation")

Applying the algorithm with ε = 170 gives:

.. plot::

    from algolab.plot import plot_algo
    from algolab.simplify import anglereduce
    plot_algo(anglereduce, 0, "After Anglereduce with epsilon=170", [170])

And applying the algorithm with ε = 150 gives:

.. plot::

    from algolab.plot import plot_algo
    from algolab.simplify import anglereduce
    plot_algo(anglereduce, 0, "After Anglereduce with epsilon=150", [150])

.. _simp_rdp:

Ramer-Douglas-Peucker
---------------------

.. autofunction:: algolab.simplify.rdp

Examples: Given the following initial situation:

.. plot::

    from algolab.plot import plot_algo
    plot_algo(lambda x: x, 0, "Initial Situation")

Applying the algorithm with ε = 0.5 gives:

.. plot::

    from algolab.plot import plot_algo
    from algolab.simplify import rdp
    plot_algo(rdp, 0, "After RDP with epsilon=0.5", [0.5])

And applying the algorithm with ε = 1.5 gives:

.. plot::

    from algolab.plot import plot_algo
    from algolab.simplify import rdp
    plot_algo(rdp, 0, "After RDP with epsilon=1.5", [1.5])
