class Segmenter(object):
    """
    Base class for all segmentation algorithms.
    """
    @property
    def estimated_num_segments(self):
        raise NotImplementedError("Segmenter needs to implement this.")

    @property
    def segments(self):
        raise NotImplementedError("Segmenter needs to implement this.")

    @property
    def segments_as_triplets(self):
        """
        Equal to :py:obj:`.segments`, except that this is a list
        of triplets (lon, lat, id).
        """
        for segment in self.segments:
            yield [n["loc"] + [n["_id"]] for n in segment]

    @property
    def segments_as_coordinates(self):
        """
        Equal to :py:obj:`.segments`, except that this is a list
        of triplets (lon, lat).
        """
        for segment in self.segments:
            yield [n["loc"] for n in segment]

    @property
    def segment_ids(self):
        """
        Equal to :py:obj:`.segments`, except that this is a list
        of ids.
        """
        for segment in self.segments:
            yield [n["_id"] for n in segment]


from algolab.segment.essegmenter import ESSegmenter, CESSegmenter

__all__ = ['CESSegmenter', 'ESSegmenter', 'Segmenter']
