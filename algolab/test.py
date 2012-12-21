"""
Testing Utilities.
"""
import random
import string

from pymongo import Connection

from algolab.data import npoints
from algolab.db import create_rg

db = Connection("127.0.0.1", 27017)["osm-data"]
col = db["test"]


def randcol():
    return col["".join([random.choice(
        string.ascii_lowercase) for x in range(0, 6)])]


def rg_from_datasets(datasets, col=None):
    col = randcol() if not col else col
    for i in datasets:
        create_rg(npoints[i], col)
    return col
