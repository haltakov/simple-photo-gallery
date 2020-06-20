import os
import json
from collections import OrderedDict


class BaseGalleryLogic:
    """
    Base class for defining a gallery logic. Derived classes should implement the methods create_thumbnails and
    generate_images_data to define the specific logic.
    """

    def __init__(self, gallery_config):
        """
        Initializes the gallery logic
        :param gallery_config: Gallery config dictionary as read from the gallery.json
        """
        self.gallery_config = gallery_config

    def create_thumbnails(self, force=False):
        """
        Checks if every image has an existing thumbnail and generates it if needed (or if forced by the user)
        :param force: Forces generation of thumbnails if set to true
        """
        pass

    def generate_images_data(self, images_data):
        """
        Generate the metadata for each image
        :param images_data: Images data dictionary containing the existing metadata of the images and which will be
        updated by this function
        :return updated images data dictionary
        """
        return images_data

    def create_images_data_file(self):
        """
        Creates or updates the images_data.json file with metadata for each image (e.g. size, description and thumbnail)
        """
        images_data_path = self.gallery_config["images_data_file"]

        # Load the existing file or create an empty dict
        if os.path.exists(images_data_path):
            with open(images_data_path, "r") as images_data_in:
                images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)
        else:
            images_data = {}

        # Generate the images data
        self.generate_images_data(images_data)

        # Write the data to the JSON file
        with open(images_data_path, "w", encoding="utf-8") as images_out:
            json.dump(images_data, images_out, indent=4, separators=(",", ": "))
