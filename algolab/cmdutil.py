from __future__ import division, print_function

import sys
import logging
from contextlib import contextmanager
from datetime import datetime

log = logging.getLogger(__name__)


def require_col(db, zls):
    if type(zls) == int:
        zls = [zls]

    if type(zls) == str:
        zls = [zls]

    for zl in zls:
        if type(zl) == int:
            if db["railway_graph_" + str(zl)].count() == 0:
                die("This step requires railway_graph_%i to be present." % zl)
        else:
            if db[zl].count == 0:
                die("This step requires %s to be present." % zl)


def die(msg):
    """
    Print msg to stderr and exit with exit code 1.

    :param msg: msg to print
    :type msg: str
    """
    print(msg, file=sys.stderr)
    sys.exit(1)


@contextmanager
def log_progress(name, log_function=log.info):
    log_function("-" * 50)
    log_function("=> Starting step '%s'" % name)
    now = datetime.now()
    yield
    log_function("<= Step '%s' finished (took %s)." % (
        name, datetime.now() - now))


def log_change(u, v, log_function=log.info):
    change = ((v - u) / v) * 100 if v is not 0 else 0
    log_function("Reduced to %i nodes from %i nodes. "
                 "Change: -%i (-%.3f%%)" % (u, v, v - u, change))


@contextmanager
def timing(name):
    """
    Context manager to measure execution time.
    """
    start = datetime.now()
    yield
    end = datetime.now()
    print('Executing %s took %.2f seconds' % (name, (end - start).total_seconds()))
