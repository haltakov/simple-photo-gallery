import argparse
import os
import sys
import glob
import shutil
import json
from distutils.dir_util import copy_tree
import pkg_resources
import simplegallery.common as spg_common
import simplegallery.logic.gallery_logic as gallery_logic


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = """Initializes a new Simple Photo Gallery in the specified folder (default is the current folder).
    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery"""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "remote_link",
        metavar="URL",
        nargs="?",
        default="",
        help="Link to a remote shared album (OneDrive or Google Photos supported)",
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path to the folder which will be turned into a gallery",
    )

    parser.add_argument(
        "--image-source",
        dest="image_source",
        action="store",
        default=None,
        help="Path to a directory from where the images should be copied into the gallery.",
    )

    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Overrides existing config and template files files",
    )

    parser.add_argument(
        "--keep-gallery-config",
        dest="keep_gallery_config",
        action="store_true",
        help="Use to copy the template files only, without generating a gallery.json",
    )

    return parser.parse_args()


def check_if_gallery_creation_possible(gallery_root):
    """
    Checks if a gallery can be created in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a new gallery can be created and false otherwise
    """

    # Check if the path exists
    if not os.path.exists(gallery_root):
        spg_common.log(f"The specified gallery path does not exist: {gallery_root}.")
        return False

    return True


def check_if_gallery_already_exists(gallery_root):
    """
    Checks if a gallery already exists in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a gallery exists and false otherwise
    """

    paths_to_check = [
        os.path.join(gallery_root, "gallery.json"),
        os.path.join(gallery_root, "images_data.json"),
        os.path.join(gallery_root, "templates"),
        os.path.join(gallery_root, "public"),
    ]

    # Check if any of the paths exists
    for path in paths_to_check:
        if os.path.exists(path):
            return True

    return False


def create_gallery_folder_structure(gallery_root, image_source):
    """
    Creates the gallery folder structure by copying all the gallery templates and moving all images and videos to the
    photos subfolder
    :param gallery_root: Path to the gallery root
    """

    # Copy the public and templates folder
    spg_common.log("Copying gallery template files...")
    copy_tree(
        pkg_resources.resource_filename("simplegallery", "data/templates"),
        os.path.join(gallery_root, "templates"),
    )
    copy_tree(
        pkg_resources.resource_filename("simplegallery", "data/public"),
        os.path.join(gallery_root, "public"),
    )

    # Move all images and videos to the correct subfolder under public
    photos_dir = os.path.join(gallery_root, "public", "images", "photos")
    spg_common.log(f"Moving all photos and videos to {photos_dir}...")

    only_copy = True
    if not image_source:
        image_source = gallery_root
        only_copy = False
    for path in glob.glob(os.path.join(image_source, "*")):
        basename_lower = os.path.basename(path).lower()
        if (
            basename_lower.endswith(".jpg")
            or basename_lower.endswith(".jpeg")
            or basename_lower.endswith(".gif")
            or basename_lower.endswith(".mp4")
            or basename_lower.endswith(".png")
        ):
            if only_copy:
                shutil.copy(path, os.path.join(photos_dir, os.path.basename(path)))
            else:
                shutil.move(path, os.path.join(photos_dir, os.path.basename(path)))


def create_gallery_json(gallery_root, remote_link):
    """
    Creates a new gallery.json file, based on settings specified by the user
    :param gallery_root: Path to the gallery root
    :param remote_link: Optional link to a remote shared album containing the photos for the gallery
    """

    spg_common.log("Creating the gallery config...")
    spg_common.log(
        "You can answer the following questions in order to set some important gallery properties. You can "
        "also just press Enter to leave the default and change it later in the gallery.json file."
    )

    # Initialize the gallery config with the main gallery paths
    gallery_config = dict(
        images_data_file=os.path.join(gallery_root, "images_data.json"),
        public_path=os.path.join(gallery_root, "public"),
        templates_path=os.path.join(gallery_root, "templates"),
        images_path=os.path.join(gallery_root, "public", "images", "photos"),
        thumbnails_path=os.path.join(gallery_root, "public", "images", "thumbnails"),
        thumbnail_height=160,
    )

    # Initialize remote gallery configuration
    if remote_link:
        remote_gallery_type = gallery_logic.get_gallery_type(remote_link)

        if not remote_gallery_type:
            raise spg_common.SPGException(
                "Cannot initialize remote gallery - please check the provided link."
            )
        else:
            gallery_config["remote_gallery_type"] = remote_gallery_type
            gallery_config["remote_link"] = remote_link

    # Set configuration defaults
    default_title = "My Gallery"
    default_description = "Default description of my gallery"

    # Ask the user for the title
    gallery_config["title"] = (
        input(f'What is the title of your gallery? (default: "{default_title}")\n')
        or default_title
    )

    # Ask the user for the description
    gallery_config["description"] = (
        input(
            f'What is the description of your gallery? (default: "{default_description}")\n'
        )
        or default_description
    )

    # Ask the user for the background image
    gallery_config["background_photo"] = input(
        f'Which image should be used as background for the header? (default: "")\n'
    )

    # Ask the user for the site URL
    gallery_config["url"] = input(
        f'What is your site URL? This is only needed to better show links to your galleries on social media (default: "")\n'
    )

    # Set the default background offset right after the background image
    gallery_config["background_photo_offset"] = 30

    # Save the configuration to a file
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    with open(gallery_config_path, "w", encoding="utf-8") as out:
        json.dump(gallery_config, out, indent=4, separators=(",", ": "))

    spg_common.log("Gallery config stored in gallery.json")


def main():
    """
    Initializes a new Simple Photo Gallery in a specified folder
    """

    # Parse the arguments
    args = parse_args()

    # Get the gallery root from the arguments
    gallery_root = args.path

    # Get the image source directory
    image_source = args.image_source

    # Check if a gallery can be created at this location
    if not check_if_gallery_creation_possible(gallery_root):
        sys.exit(1)

    # Check if the specified gallery root already contains a gallery
    if check_if_gallery_already_exists(gallery_root):
        if not args.force:
            spg_common.log(
                "A Simple Photo Gallery already exists at the specified location. Set the --force parameter "
                "if you want to overwrite it."
            )
            sys.exit(0)
        else:
            spg_common.log(
                "A Simple Photo Gallery already exists at the specified location, but will be overwritten."
            )
    spg_common.log("Creating a Simple Photo Gallery...")

    # Create the gallery json file
    try:
        if not args.keep_gallery_config:
            create_gallery_json(gallery_root, args.remote_link)
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while creating the gallery.json file: {str(exception)}"
        )
        sys.exit(1)

    # Copy the template files to the gallery root
    try:
        create_gallery_folder_structure(gallery_root, image_source)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the gallery structure: {str(exception)}"
        )
        sys.exit(1)

    spg_common.log("Simple Photo Gallery initialized successfully!")


if __name__ == "__main__":
    main()
