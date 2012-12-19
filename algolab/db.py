from pymongo import GEO2D

from algolab.util import gcdist, raise_or_return


def node_for(_id, col):
    """
    Returns the node from a collection `col` identified
    by a given `_id`.

    :param _id: the id of the node
    :type _id: integer
    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: a node
    :raise: :exc:`ValueError` if there is no such node
    """
    return raise_or_return(col.find_one(_id),
            ValueError, "There is no such node %s" % _id)


def loc_for(_id, col):
    """
    Returns a 3-tuple (lon, lat, id) for the node
    identified by `_id` from the collection `col`.

    :param _id: the id of the node
    :type _id: integer
    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: 3-tuple (lon, lat, id)
    :raise: :exc:`ValueError` if there is no such node
    """
    return node_for(_id, col)["loc"] + [_id]


def locs_for(_ids, col):
    """
    Applies `~algolab.db.loc_for` for each id in `_ids`.

    :param _ids: list of the ids of the nodes
    :type _id: list of integers
    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: a list of 3-tuples (lon, lat, id)
    :raise: :exc:`ValueError` if there is no such node
    """
    return [loc_for(i, col) for i in _ids]


def extend_neighbors(node1, node2):
    """
    Extends `node1`'s neighbors with those of `node2`.

    :param node1: the node to extend
    :param node2: the node to extend `node1` with
    """
    for n in node2["successors"]:
        if n["id"] not in [a["id"] for a in node1["successors"]]:
            node1["successors"].append(n)


def remove_neighbors(node, neighbor_ids):
    """
    Removes the neighbors identified by `neighbor_ids`
    from a node.

    :param node: the node to remove the neighbors from
    :param neighbor_ids: the ids of the neighbors to remove
    :type neighbor_ids: list
    """
    node["successors"] = filter(
            lambda s: s["id"] not in neighbor_ids,
            node["successors"])


def nodes_with_num_neighbors_gt(col, num):
    """
    Find all nodes that have more than `num` neighbors.
    """
    return col.find({"$where": "this.successors.length > %s" % num})


def intersections(col):
    """
    Finds intersections/crossings in a railway graph.
    """
    return nodes_with_num_neighbors_gt(col, 2)


def nodes_with_num_neighbors(col, num):
    return col.find({"successors": {"$size": num}})


def nodes_with_num_neighbors_ne(col, num):
    # TODO: Maybe this can be made faster by not using JavaScript
    return col.find({"$where": "this.successors.length != %s" % num})


def endpoints(col):
    """
    Finds endpoints in a railway graph.
    """
    return nodes_with_num_neighbors(col, 1)


def inconsistent_edges(col):
    """
    Returns edges that lead to a non-existing node.
    """
    result = set()

    for node in col.find():
        for successor_id in node["successors"]:
            successor = col.find_one(successor_id)
            if not successor:
                result.add((node["_id"], successor_id))

    return result


def empty(col):
    """
    Empties a collection and creates a :class:`GEO2D` index.
    """
    col.drop()
    col.create_index([("loc", GEO2D)])


def merge_nodes(rg, node_id, merge_with_ids, distance_function=gcdist):
    """
    Merges all nodes identified by their id (`merge_with_ids`) with
    a node identified by `node_id`.

    Also takes care of the nodes who are neighbors of the node we are
    going to merge with.
    """
    node = rg.find_one(node_id)

    visit_ids = set()

    for merge_id in merge_with_ids:
        merge = rg.find_one(merge_id)
        extend_neighbors(node, merge)

        for s in merge["successors"]:
            visit_ids.add(s["id"])
        rg.remove(merge["_id"])

    remove_neighbors(node, merge_with_ids + [node_id])

    for visit_id in visit_ids:
        # Visit all of the duplication's neighbors
        visit = rg.find_one(visit_id)
        visit["successors"] = filter(
                lambda x: x["id"] not in merge_with_ids, visit["successors"])
        visit["successors"].append({
            "id": node_id,
            "distance": int(distance_function(node["loc"], visit["loc"]))})
        rg.save(visit)

    rg.save(node)


def dedup(rg, distance_function=gcdist):
    """
    Removes all duplicates from a railway graph `rg`.

    Two points are duplicates of each other if they have the same location.
    """
    duplicates = set()
    duplicates_map = {}

    for node in rg.find():
        if node["_id"] in duplicates:
            continue
        for dup in rg.find({"loc": node["loc"]}):
            if dup["_id"] != node["_id"]:
                # `dup` is a duplicate of `node`
                duplicates.add(dup["_id"])
                if node["_id"] in duplicates_map:
                    duplicates_map[node["_id"]].append(dup["_id"])
                else:
                    duplicates_map[node["_id"]] = [dup["_id"]]

    for node_id, merge_with_ids in duplicates_map.items():
        merge_nodes(rg, node_id, merge_with_ids, distance_function)

    return len(duplicates)


def create_rg_from(node_ids, source_col, dest_col):
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


def create_rg(points, col, distance_function=gcdist):
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
                "id": points[i - 1][2],
                "distance": int(distance_function(point[:2], points[i - 1][:2]))})

        if i < len(points) - 1:
            neighbors.append({
                "id": points[i + 1][2],
                "distance": int(distance_function(point[:2], points[i + 1][:2]))})

        existing_node = col.find_one(point[2])
        if existing_node:
            extend_neighbors(existing_node, {"successors": neighbors})
            col.save(existing_node)
        else:
            col.insert({
                "_id": point[2],
                "loc": point[:2],
                "successors": neighbors,
            })
