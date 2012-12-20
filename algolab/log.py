import logging

FORMAT = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S"


def configure_logging():
    logging.basicConfig(format=FORMAT)
