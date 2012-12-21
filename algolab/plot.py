# -*- coding: utf-8 -*-
"""
Plotting helpers.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from algolab.data import npoints, points
import pylab as pl


def plot_algo(algo, dataset_id, title, *args):
        pl.title(title)
        result = algo(npoints[dataset_id], *args)
        pl.plot(zip(*result)[0], zip(*result)[1], 'o-')
        return pl
