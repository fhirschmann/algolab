import logging

FORMAT = "[%(asctime)s] %(message)s"


def configure_logging():
    logging.basicConfig(format=FORMAT)
