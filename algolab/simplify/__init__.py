import os
import sys

from algolab.db import create_rg
from algolab.segment import Segmenter

from algolab.simplify.rdp import rdp
from algolab.simplify.anglered import anglereduce

__all__ = ['simplify', 'rdp', 'anglereduce']


def simplify(algo, source_col, dest_col, args=[], segmenter=Segmenter,
             progress=True):
    segmenter = Segmenter(source_col)

    n = segmenter.estimated_num_segments

    for i, seg in enumerate(segmenter.segments_as_triplets):
        if progress:
            sys.stdout.write("\rApplying %s to segment %i of %i" % (
                algo.__name__, i, n))

        create_rg(algo(seg, *args), dest_col)

    print(os.linesep)
