# -*- coding: utf-8 -*-
"""
Plotting helpers.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from algolab.data import npoints, points
from algolab.segment import Segmenter

import pylab as pl


def plot_algo(algo, dataset_id, title, *args):
        pl.title(title)
        result = algo(npoints[dataset_id], *args)
        pl.plot(zip(*result)[0], zip(*result)[1], 'o-')
        return pl


def plot_datasets(datasets, title=None):
    title = title if title else "Datasets " + ",".join(
        [str(d) for d in datasets])
    pl.title(title)

    for i in datasets:
        pl.plot(zip(*points[i])[0], zip(*points[i])[1], 'o-')
    return pl


def plot_rg(rg, title):
    pl.title(title)
    segments = Segmenter(rg).segments_as_triplets
    for s in segments:
        pl.plot(zip(*s)[0], zip(*s)[1], 'ro-')
