import json


class SPGException(Exception):
    """Exception raised for errors during the createion of the Simple Photo Gallery.

    Attributes:
        message -- explanation of the error that will be shown to the user
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


def log(message):
    """
    Log a message to the console
    :param message: message string
    """
    print(message)


def read_gallery_config(gallery_path):
    """
    Read the gallery config from the gallery.json file
    :param gallery_path: path to the JSON file
    :return: dict containing the gallery config
    """
    try:
        with open(gallery_path, "r") as gallery_in:
            return json.load(gallery_in)
    except OSError:
        return []
