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


def create_node(node, neighbor_nodes=[]):
    """
    Creates a new dictionary, a node with its neighbors, that can be
    inserted into a `~pymongo.collection.Collection`.

    :param node: a node
    :type node: dictionary
    :param neighbor_nodes: list of neighbors
    :type neighbor_nodes: list of dicts
    """
    return {
            "_id": node["_id"],
            "loc": node["loc"],
            "successors": [{
                "id": n["_id"],
                "distance": node_distance(node, n)
            } for n in neighbor_nodes]
        }


def node_distance(node1, node2):
    """
    Calculates the distance between two nodes in the database.
    """
    return edist(node2["loc"], node2["loc"])


def apply_reduction(node_ids, source_col, dest_col):
    """
    Reads all nodes identified by their `ids` from `source_col` and
    writes them to the `dest_col`.

    If the source or destination node already exists, it is modified
    to include the new neighbors.

    The node ids will not be changed.

    This method also calculates the distance between the newly created
    notes in `dest_col`.

    :param node_ids: list of node ids in a segment to keep
    :type node_ids: list of integers
    :param source_col: the collection to read from
    :type source_col: a :class:`~pymongo.collection.Collection`
    :param dest_col: the collection to read from
    :type dest_col: a :class:`~pymongo.collection.Collection`
    """
    if len(node_ids) < 2:
        raise ValueError("At least two points are required.")

    for i, node_id in enumerate(node_ids):
        neighbors = []

        if i > 0:
            neighbors.append(node_for(node_ids[i - 1], source_col))

        if i < len(node_ids) - 1:
            neighbors.append(node_for(node_ids[i + 1], source_col))

        dest_col.insert(create_node(node_for(node_id, source_col), neighbors))


def create_rg(points, col):
    """
    Creates a railway graph from a given sequence of `points`
    and write it to a collection `col`.

    :param col: a collection cursor
    :type col : a :class:`~pymongo.collection.Collection`
    """
    if len(points) < 2:
        raise ValueError("At least two points are required.")

    for i, point in enumerate(points):
        neighbors = []
        if i > 0:
            neighbors.append({"id": i - 1, "distance": edist(point[:2], points[i - 1][:2])})
        if i < len(points) - 1:
            neighbors.append({"id": i + 1, "distance": edist(point[:2], points[i + 1][:2])})

        existing_node = col.find_one({"loc": point})
        if existing_node:
            col.update(
                    {"_id": point[2]},
                    {"successors": existing_node["successors"] + neighbors})
        else:
            col.insert({
                "_id": point[2],
                "loc": point[:2],
                "successors": neighbors,
            })
