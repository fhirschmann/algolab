# -*- coding: utf-8 -*-
"""
Database-related utilities.

.. moduleauthor:: Fabian Hirschmann <fabian@hirschm.net>
"""
import logging
import os
import sys

from pymongo import GEO2D
from bson.code import Code

from algolab.util import distance

log = logging.getLogger(__name__)


def node_for(id_, col):
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
    node = col.find_one(id_)
    if node is None:
        log.error("No such node: %s" % id_)

    return node


def loc_for(id_, col):
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
    return node_for(id_, col)["loc"] + [id_]


def locs_for(ids_, col):
    """
    Applies :func:`~algolab.db.loc_for` for each id in `_ids`.

    :param _ids: list of the ids of the nodes
    :type _id: list of integers
    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: a list of 3-tuples (lon, lat, id)
    :raise: :exc:`ValueError` if there is no such node
    """
    return [loc_for(i, col) for i in ids_]


def neighbors(node):
    """Return the list of successor node ids of node."""
    return [s["id"] for s in node["successors"]]


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

    You still NEED TO save the node afterwards.

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

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: a collection cursor
    """
    return col.find({"$where": "this.successors.length > %s" % num})


def intersections(col):
    """
    Finds intersections/crossings in a railway graph.

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: a collection cursor
    """
    return nodes_with_num_neighbors_gt(col, 2)


def nodes_with_num_neighbors(col, num):
    return col.find({"successors": {"$size": num}})


def nodes_with_num_neighbors_ne(col, num):
    """
    Find nodes that don't have `num` neighbors.

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :param num: number of neighbors
    :type num: integer
    :returns: a collection cursor
    """
    # TODO: Maybe this can be made faster by not using JavaScript
    return col.find({"$where": "this.successors.length != %s" % num})


def endpoints(col):
    """
    Finds endpoints in a railway graph.

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    """
    return nodes_with_num_neighbors(col, 1)


def inconsistent_edges(col):
    """
    Returns edges that lead to a non-existing node.

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :return: a list of tuples (a, b) where a -> b is an edge
    """
    result = set()

    for node in col.find():
        for succ in node["successors"]:
            successor = col.find_one(succ["id"])
            if not successor:
                result.add((node["_id"], succ["id"]))

    return result


def remove_edge(col, node, neighbor_id):
    """
    Removes the edge from a `node` to a neighbor identified
    by `neighbor_id`.

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :param node: the node
    :param neighbor_id: the id of the neighbor
    """
    node["successors"] = [s for s in node["successors"] if s["id"] != neighbor_id]
    col.save(node)


def empty(col):
    """
    Empties a collection and creates a :class:`~pymongo.GEO2D` index.

    :param col: the collection to read from
    :type col: a :class:`~pymongo.collection.Collection`
    :returns: the new collection
    """
    col.drop()
    col.create_index([("loc", GEO2D)])

    return col
new = empty


def copy(source_col, dest_col):
    """
    Copies a collection from `source_col` to `dest_col`.

    WARNING: This will erase all data storted in `dest_col`.

    :param source_col: the source collection
    :param dest_col: the destination collection
    """
    empty(dest_col)

    for node in source_col.find():
        dest_col.insert(dict(node))
    log.debug("Copied %i nodes from '%s' to '%s'" % (dest_col.count(),
                 source_col.name, dest_col.name))


def recalculate_distances(rg, progress=True):
    """
    Recalculates the distance between nodes in a given
    railway graph `rg`.

    :param rg: a collection cursor to a railway graph
    :type rg: a :class:`~pymongo.collection.Collection`
    :param progress: whether or not to show progress
    :type progress: boolean
    """
    count = rg.count()
    for i, node in enumerate(rg.find()):
        for neighbor in node["successors"]:
            neighbor_node = rg.find_one(neighbor["id"])
            neighbor["distance"] = distance(
                node["loc"], neighbor_node["loc"])
        rg.save(node)

        if progress:
            sys.stdout.write("\rProgress: %d of %d" % (i, count))

    if progress:
        print(os.linesep)


def merge_nodes(rg, node_id, merge_with_ids):
    """
    Merges all nodes identified by their id (`merge_with_ids`) with
    a node identified by `node_id`.

    Also takes care of the nodes who are neighbors of the node we are
    going to merge with.

    :param rg: the railway graph (collection) to work on
    :type rg: a :class:`~pymongo.collection.Collection`
    :param node_id: the id of the node that survives
    :type node_id: integer
    :param merge_with_ids: iterable of node ids to merge with
    :type merge_with_ids: iterable of integers
    """
    node = rg.find_one(node_id)

    new_successors = set()

    for merge_id in merge_with_ids:
        merge = rg.find_one(merge_id)
        new_successors.update(neighbors(merge))
        rg.remove(merge_id)

    node_ids = set(merge_with_ids)
    node_ids.add(node_id)
    new_successors -= node_ids
    node['successors'] = [s for s in node['successors']
                          if s['id'] not in node_ids.union(new_successors)]

    # remove backpointers of merged nodes
    for successor_id in new_successors:
        successor = rg.find_one(successor_id)
        if not successor:
            logging.error("%i's neighbor %i does not exist.",
                          node_id, successor_id)
            continue
        successor['successors'] = [s for s in successor['successors']
                                   if s['id'] not in node_ids]
        distance_ = int(distance(node['loc'], successor['loc']))
        successor['successors'].append({'id': node_id, 'distance': distance_})
        node['successors'].append({'id': successor_id, 'distance': distance_})
        rg.save(successor)

    rg.save(node)


def dedup(rg):
    """
    Removes all duplicates from a railway graph `rg`.

    Two points are duplicates of each other if they have the same location.
    This function uses mongodb's map-reduce.

    :param rg: a collection cursor to a railway graph
    :type rg: a :class:`~pymongo.collection.Collection`
    """
    num_dups = 0
    map_ = Code("""
        function() {
            emit(this.loc.join('|'), 1);
        }
        """)
    reduce_ = Code("""
        function(key, values) {
            return Array.sum(values);
        }
        """)
    result = rg.map_reduce(map_, reduce_, "tmp_find_dups")
    loc_ids = result.find({"value": {"$gt": 1}})
    for loc_id in loc_ids:
        num_dups += loc_id["value"] - 1
        loc = [float(c) for c in loc_id["_id"].split("|")]

        dups = [n["_id"] for n in list(rg.find({"loc": loc}))]
        this = dups.pop()
        merge_nodes(rg, this, dups)

    return int(num_dups)


def delonelynize(rg):
    """
    Removes all lonely nodes (nodes without neighbors) from
    the railway graph `rg`.

    :param rg: a collection cursor to a railway graph
    :type rg: a :class:`~pymongo.collection.Collection`
    """
    nodes = nodes_with_num_neighbors(rg, 0)
    for node in nodes:
        node.remove()

    return nodes.count()


def create_rg_from(node_ids, source_col, dest_col):
    """
    Reads all nodes identified by their `ids` from `source_col` and
    writes them to the `dest_col`.

    Please see :func:`~algolab.db.create_rg` for details.

    :param node_ids: list of node ids in a segment to keep
    :type node_ids: list of integers
    :param source_col: the collection to read from
    :type source_col: a :class:`~pymongo.collection.Collection`
    :param dest_col: the collection to read from
    :type dest_col: a :class:`~pymongo.collection.Collection`
    """
    points = [(n["loc"][0], n["loc"][1], n["_id"]) for n in
            source_col.find({"_id": {"$in": node_ids}})]
    return create_rg(points, dest_col)


def create_rg(points, col):
    """
    Creates a railway graph from a given sequence of `points`
    and writes it to a collection `col`.

    If a node already exists, it is modified to include the new
    neighbors.

    The node ids will not be changed.

    This method also calculates the distance between the newly created
    nodes in `col`.

    This method is usually called for each segment that has been
    simplified by :func:`~algolab.simplify.rdp` or similar algorithms.

    :param points: a curve that is approximated by a series of points
    :type points: list of 3-tuples (x, y, id)
    :param col: a collection cursor
    :type col: a :class:`~pymongo.collection.Collection`
    """
    if len(points) < 2:
        raise ValueError("At least two points are required.")

    for i, point in enumerate(points):
        neighbors = []

        # node has a predecessor
        if i > 0:
            neighbors.append({
                "id": points[i - 1][2],
                "distance": int(distance(point[:2], points[i - 1][:2]))})

        # node has a successor
        if i < len(points) - 1:
            neighbors.append({
                "id": points[i + 1][2],
                "distance": int(distance(point[:2], points[i + 1][:2]))})

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
