import logging


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger for the building block.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)-8s %(filename)s - %(message)s",
    "%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger


