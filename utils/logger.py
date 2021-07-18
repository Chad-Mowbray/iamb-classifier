import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


def args_logger(func):
    def inner(*args, **kwargs):
        logging.info("f: " + func.__name__ + " -- args: " + str(args) + ", kwargs: " + str(kwargs))
        return func(*args, **kwargs)
    return inner


