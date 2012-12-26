# -*- coding: utf-8 -*-
"""
Plotting helpers.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
from algolab.data import npoints, points
from algolab.segment import ESSegmenter

import pylab as pl


def plot_algo(algo, dataset_id, title, algo_args=[]):
    """
    Plots a line simplification algorithm.

    :param algo: algorithm to plot
    :type algo: function
    :param dataset_ids: list of datasets to plot
    :type dataset_ids: list of integers
    :param title: title of the plot
    :type title: string
    :param algo_args: arguments to pass to the algorithm
    :type algo_args: list of arguments
    """
    pl.title(title)
    result = algo(npoints[dataset_id], *algo_args)
    pl.plot(zip(*result)[0], zip(*result)[1], 'o-')
    return pl


def plot_datasets(dataset_ids, title=None):
    """
    Plots one or more dataset.

    :param dataset_ids: list of datasets to plot
    :type dataset_ids: list of integers
    :param title: title of the plot
    :type title: string
    """
    title = title if title else "Datasets " + ",".join(
        [str(d) for d in dataset_ids])
    pl.title(title)

    for i in dataset_ids:
        pl.plot(zip(*points[i])[0], zip(*points[i])[1], 'o-')
    return pl


def plot_rg(rg, title):
    """
    Plots a railway graph.
    """
    pl.title(title)
    segments = ESSegmenter(rg).segments_as_triplets
    for s in segments:
        pl.plot(zip(*s)[0], zip(*s)[1], 'ro-')
