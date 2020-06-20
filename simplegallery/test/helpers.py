import os
import sys
import json
from PIL import Image
import simplegallery.gallery_init as gallery_init


def init_gallery_and_read_gallery_config(path, remote_link=""):
    """
    Initializes a new gallery and reads the data from the gallery.json file
    :param path: path to the folder where the gallery will be created
    :param remote_link: optional remote link to initialize a remote gallery
    :return: gallery config dict
    """

    sys.argv = ["gallery_init", remote_link, "-p", path]
    gallery_init.main()

    with open(os.path.join(path, "gallery.json"), "r") as json_in:
        gallery_config = json.load(json_in)

    return gallery_config


def check_image_data(
    test, images_data, image_name, description, size, thumbnail_size, local_files=False
):
    """
    Checks if images data contains the specified image with all attributes set correctly
    :param test: unit test object
    :param images_data: images data dictionary
    :param image_name: image name to look for in images_data
    :param description: image description to check
    :param size: image size to check
    :param thumbnail_size: thumbnail size to check
    :param local_files: if True the path to the image is checked as a local file, otherwise it is checked as a URL
    """
    image_data = images_data[image_name]
    test.assertEqual(description, image_data["description"])
    test.assertTrue(image_data["mtime"])
    test.assertEqual(size, image_data["size"])
    test.assertEqual(thumbnail_size, image_data["thumbnail_size"])
    test.assertEqual("image", image_data["type"])
    if local_files:
        test.assertEqual(
            os.path.join("images", "photos", image_name), image_data["src"]
        )
        test.assertEqual(
            os.path.join("images", "thumbnails", image_name), image_data["thumbnail"]
        )
    else:
        test.assertTrue(image_name in image_data["src"])
        test.assertTrue(image_name in image_data["thumbnail"])


def create_mock_image(path, width, height):
    """
    Creates a mock image with a red color
    :param path: path where the image should be stored
    :param width: width of the image
    :param height: height of the image
    """
    if (
        path.lower().endswith(".jpg")
        or path.lower().endswith(".jpeg")
        or path.lower().endswith(".png")
    ):
        img = Image.new("RGB", (width, height), color="red")
    elif path.lower().endswith(".gif"):
        img = Image.new("P", (width, height), color="red")
    else:
        raise RuntimeError("Unsupported image type")

    img.save(path)
    img.close()
