def apply_reduction(ids, source_col, dest_col):
    """
    Reads all nodes identified by their `ids` from `source_col` and
    writes them to the `dest_col`.

    If the source or destination node already exists, it is modified
    to include the new neighbors.

    :param ids: list of ids in a segment to keep
    :type ids: list of integers
    :param source_col: the collection to read from
    :type source_col: a :class:`~pymongo.collection.Collection`
    :param dest_col: the collection to read from
    :type dest_col: a :class:`~pymongo.collection.Collection`
    """
    pass
