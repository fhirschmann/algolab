from __future__ import division, print_function

import sys
import logging
from contextlib import contextmanager
from datetime import datetime

log = logging.getLogger(__name__)


def require_col(db, zls):
    """
    Make sure all collections `zls` are present in `db` and abort the program if
    not.

    :param db: connection that should contain required collections
    :type db: :class:`pymongo.Connection`
    :param zls: required collections
    :type zls: int, str or sequence of int or str
    """
    if isinstance(zls, (int, str)):
        zls = [zls]

    zls = [('railway_graph_%d' % zl) if isinstance(zl, int) else zl for zl in zls]
    empty_collections = [zl for zl in zls if db[zl].count() == 0]
    if empty_collections:
        die('This step requires the collections %s to be present'
            % ', '.join(empty_collections))


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


def log_change(after, before, log_function=log.info):
    change = ((before - after) / before) * 100 if before is not 0 else 0
    log_function("Reduced to %i nodes from %i nodes. "
                 "Change: -%i (-%.3f%%)" % (after, before, before - after, change))


@contextmanager
def timing(name):
    """
    Context manager to measure execution time.
    """
    start = datetime.now()
    yield
    end = datetime.now()
    print('Executing %s took %.2f seconds' % (name, (end - start).total_seconds()))


def defaultparser():
    """
    Creates and returns a default command line parser with `description` and
    the following arguments: --host, --port, --db, --debug, --quiet.

    You can add this as your parent parser by passing `parents=[defaultparser]`
    to your :class:`~argparse.ArgumentParser`.

    :param description: description of the parser
    :type description: string
    """
    import argparse
    from algolab.log import FORMAT as LOGGING_FORMAT

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--host", action="store", dest="host", default="127.0.0.1",
            type=str, help="host of the mongodb server")
    parser.add_argument("--port", action="store", dest="port", default=27017,
            type=int, help="port of the mongodb server")
    parser.add_argument("--db", action="store", dest="db", default="osm-data",
            type=str, help="name of the database")
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument("-d", "--debug",
            action="store_const", const=logging.DEBUG,
            dest="loglevel", default=logging.INFO,
            help="print debugging messages")
    log_group.add_argument("-q", "--quiet",
            action="store_const", const=logging.WARNING,
            dest="loglevel", help="suppress most messages")
    args, _ = parser.parse_known_args()
    logging.basicConfig(level=args.loglevel, format=LOGGING_FORMAT)

    return parser
