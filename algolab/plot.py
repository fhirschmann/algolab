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


def plot_datasets(dataset_ids, title=None, legend=True, labels=True):
    """
    Plots one or more dataset.

    :param dataset_ids: list of datasets to plot
    :type dataset_ids: list of integers
    :param title: title of the plot
    :type title: string
    :param legend: whether or not to show legend
    :type legend: boolean
    :param labels: whether or not to plot point labels
    :type labels: boolean
    """
    title = title if title else "Datasets " + ",".join(
        [str(d) for d in dataset_ids])
    pl.title(title)

    data = {k: v for k, v in npoints.items() if k in dataset_ids}

    lines = [pl.plot(zip(*p)[0], zip(*p)[1], 'o-')[0] for p in data.values()]

    if legend:
        pl.legend(lines, data.keys())

    if labels:
        for x, y, l in [i for s in data.values() for i in s]:
            pl.annotate(str(l), xy=(x, y), xytext=(x, y + 0.1))

    pl.grid(True)

    return pl


def plot_rg(rg, title):
    """
    Plots a railway graph.
    """
    pl.title(title)
    segments = ESSegmenter(rg).segments_as_triplets
    for s in segments:
        pl.plot(zip(*s)[0], zip(*s)[1], 'ro-')
