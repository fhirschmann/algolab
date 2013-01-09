def rminner(points):
    """
    Removes all inner points from a line segment.

    In other words, this algorithm deletes all points but
    the start- and endpoint.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, id)
    """
    return [points[0], points[-1]]
