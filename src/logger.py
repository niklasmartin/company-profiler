import logging
import os
from google.cloud import logging as cloud_logging


def get_logger(name):
    """Creates a logger that outputs to console locally and to Cloud Logging when deployed."""
    logger = logging.getLogger(name)

    if os.getenv("GCP_PROJECT"):
        logging_client = cloud_logging.Client()
        cloud_handler = cloud_logging.handlers.CloudLoggingHandler(logging_client)
        logger.addHandler(cloud_handler)
    else:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)
    return logger
