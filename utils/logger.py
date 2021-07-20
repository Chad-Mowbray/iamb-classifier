import logging
import inspect

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


def args_logger(func):
    def inner(*args, **kwargs):
        # logging.info(func.__qualname__ + " -- args: " + str(args) + ", kwargs: " + str(kwargs))
        return func(*args, **kwargs)
    return inner


