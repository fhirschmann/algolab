from __future__ import print_function, division
import os

from algolab.db import create_rg
from algolab.util import ll2xy
from algolab.segment import ESSegmenter

from algolab.simplify.rdp import rdp
from algolab.simplify.anglered import anglereduce
from algolab.simplify.rminner import rminner

__all__ = ['simplify', 'rdp', 'anglereduce', 'rminner']


def simplify(algo, source_col, dest_col, args=[], segmenter=ESSegmenter,
             progress=True, projection=True):
    """
    Segments a railway graph using `segmenter`, applies the simplification
    algorithm `algo` with arguments `args` to `source_col` and stores the
    result in `dest_col`.

    :param algo: algorithm to use
    :type algo: function with signature algo(points, *args)
    :param source_col: the source collection
    :type source_col: a :class:`~pymongo.collection.Collection`
    :param dest_col: the destination collection
    :type dest_col: a :class:`~pymongo.collection.Collection`
    :param args: arguments to pass to `algo` (will be unpacked)
    :type args: sequence
    :param segmenter: segmenter to use
    :type segmenter: `~algolab.segment.Segmenter`
    :param progress: show progress
    :type progress: boolean
    :param projection: project points onto a map (useful if coordinates are given)
    :type projection: boolean
    """
    s = segmenter(source_col)
    n = s.estimated_num_segments

    for i, seg in enumerate(s.segments_as_triplets):
        if progress:
            print("\rApplying %s to segment %i of %i (estimated) (%.2f%%)" %
                  (algo.__name__, i, n, (i / n) * 100), end="")

        if projection:
            proj = [list(ll2xy(*p[0:2])) + [p[2]] for p in seg]
            res = algo(proj, *args)
            keep_ids = [p[2] for p in res]

            rev_proj = [p for p in seg if p[2] in keep_ids]
            create_rg(rev_proj, dest_col)
        else:
            create_rg(algo(seg, *args), dest_col)

    if progress:
        print()
