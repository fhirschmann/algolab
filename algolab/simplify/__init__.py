import os
import sys

from algolab.db import create_rg
from algolab.util import ll2xy, xy2ll
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
            sys.stdout.write("\rApplying %s to segment %i of %i" % (
                algo.__name__, i, n))

        if projection:
            # it is fair to assume all points in a segment are within
            # the same utm zone
            _, _, zone_number, zone_letter = ll2xy(*seg[0][0:2])

            proj = [list(ll2xy(*p[0:2]))[0:2] + [p[2]] for p in seg]
            res = algo(proj, *args)

            rev_proj = [list(xy2ll(p[0], p[1], zone_number, zone_letter)) + [p[2]] for p in res]
            create_rg(rev_proj, dest_col)
        else:
            create_rg(algo(seg, *args), dest_col)

    if progress:
        print(os.linesep)
