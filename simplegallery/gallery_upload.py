import argparse
import os
import sys
import simplegallery.common as spg_common
from simplegallery.upload.uploader_factory import get_uploader


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = """Uploads the gallery to a supported hosting provider. Currently supported: AWS S3 and Netlify.
                    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "hosting", metavar="HOST", default="", help="Hosting provider: aws "
    )

    parser.add_argument(
        "location",
        metavar="LOCATION",
        nargs="?",
        default="",
        help="Location at the hosting provider where the gallery should be upoaded",
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path to the folder containing the gallery.json file",
    )

    return parser.parse_args()


def main():
    """
    Uploads the gallery to the specified hosting provider
    """

    # Parse the arguments
    args = parse_args()

    # Create the uploader
    try:
        uploader = get_uploader(args.hosting)
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while preparing the upload: {str(exception)}"
        )
        sys.exit(1)

    # Read the gallery config
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    if not gallery_config:
        spg_common.log(f"Cannot load the gallery.json file ({gallery_config_path})!")
        sys.exit(1)

    # Get the location from the command line or from the gallery.json
    location = args.location
    if not location:
        if "remote_location" in gallery_config:
            location = gallery_config["remote_location"]

    # Check if the uploader location is valid
    if not uploader.check_location(location):
        spg_common.log(f"The specified location if not valid for this hosting type.")
        sys.exit(1)

    # Check if the gallery is built
    if not os.path.exists(
        os.path.join(gallery_root, gallery_config["public_path"], "index.html")
    ):
        spg_common.log(
            f"Cannot find index.html. Please build the gallery first with gallery_build.!"
        )
        sys.exit(1)

    # Upload the gallery
    try:
        uploader.upload_gallery(
            location, os.path.join(gallery_root, gallery_config["public_path"])
        )
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while uploading the gallery: {str(exception)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
