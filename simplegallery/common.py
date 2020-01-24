import logging


def setup_gallery_logging():
    """
    Configures the default logger
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-6s %(message)s')
