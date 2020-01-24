import logging
import json


class SPGException(Exception):
    """Exception raised for errors during the createion of the Simple Photo Gallery.

    Attributes:
        message -- explanation of the error that will be shown to the user
    """

    def __init__(self, message):
        self.message = message


def setup_gallery_logging():
    """
    Configures the default logger
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-6s %(message)s')


def read_gallery_config(gallery_path):
    try:
        with open(gallery_path, 'r') as gallery_in:
            return json.load(gallery_in)
    except OSError:
        return []

