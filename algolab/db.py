from algolab.util import edist


def node_for(_id, col):
    """
    Returns the node from a collection `col` identified
    by a given `_id`.

    :param _id: the id of the node
    :type _id: integer
    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    """
    return col.find_one({"_id": _id})


def node_distance(node1, node2):
    """
    Calculates the distance between two nodes in the database.
    """
    return edist(node2["loc"], node2["loc"])


def apply_reduction(node_ids, source_col, dest_col):
    """
    Reads all nodes identified by their `ids` from `source_col` and
    writes them to the `dest_col`.

    Please see `~algolab.db.create_rg` for details.

    :param node_ids: list of node ids in a segment to keep
    :type node_ids: list of integers
    :param source_col: the collection to read from
    :type source_col: a :class:`~pymongo.collection.Collection`
    :param dest_col: the collection to read from
    :type dest_col: a :class:`~pymongo.collection.Collection`
    """
    points = [(n["loc"][0], n["loc"][1], n["_id"]) for n in \
            source_col.find({"_id": {"$in": node_ids}})]
    return create_rg(points, dest_col)


def create_rg(points, col):
    """
    Creates a railway graph from a given sequence of `points`
    and write it to a collection `col`.

    If a node already exists, it is modified to include the new
    neighbors.

    The node ids will not be changed.

    This method also calculates the distance between the newly created
    nodes in `col`.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, id)
    :param col: a collection cursor
    :type col : a :class:`~pymongo.collection.Collection`
    """
    if len(points) < 2:
        raise ValueError("At least two points are required.")

    for i, point in enumerate(points):
        neighbors = []
        if i > 0:
            neighbors.append({
                "id": i - 1,
                "distance": edist(point[:2], points[i - 1][:2])})

        if i < len(points) - 1:
            neighbors.append({
                "id": i + 1,
                "distance": edist(point[:2], points[i + 1][:2])})

        existing_node = col.find_one(point[2])
        if existing_node:
            existing_node["successors"].extend(neighbors)
            col.save(existing_node)
        else:
            col.insert({
                "_id": point[2],
                "loc": point[:2],
                "successors": neighbors,
            })
