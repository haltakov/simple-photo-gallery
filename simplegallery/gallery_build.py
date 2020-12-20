import argparse
import os
import sys
import json
import jinja2
from collections import OrderedDict
import simplegallery.common as spg_common
from simplegallery.logic.gallery_logic import get_gallery_logic


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = """Generated all files needed to display the gallery (thumbnails, image descriptions and HTML page).
                    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path to the folder containing the gallery.json file",
    )

    parser.add_argument(
        "-ft",
        "--force-thumbnails",
        dest="force_thumbnails",
        action="store_true",
        help="Forces the generation of the thumbnails even if they already exist",
    )

    return parser.parse_args()


def build_html(gallery_config):
    """
    Generates the HTML file (index.html) of the gallery
    :param gallery_config: Gallery configuration dictionary
    """

    # Load the images_data
    with open(gallery_config["images_data_file"], "r") as images_data_in:
        images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)

    images_data_list = [{**images_data[image], "name": image} for image in images_data.keys()]

    # Remove descriptions if the corresponding option is enabled
    if 'disbale_captions' in gallery_config and gallery_config['disbale_captions']:
        for image in images_data:
            images_data[image]['description'] = ''

    # Find the first photo for the background if no background photo specified
    background_photo = gallery_config["background_photo"]
    if not background_photo:
        for image in images_data:
            if images_data[image]["type"] == "image":
                background_photo = image
                break

    # Collect the information for a remote gallery attribution
    remote_data = {}
    if "remote_gallery_type" in gallery_config and "remote_link" in gallery_config:
        remote_data["link"] = gallery_config["remote_link"]

        # This is not a nice place to put this, but it removes the logic out of the Jinja template, which is important
        # to keep it simple so it can be customized. A better solution is needed in the future.
        if gallery_config["remote_gallery_type"] == "google":
            remote_data["text"] = "Google Photos album"
        elif gallery_config["remote_gallery_type"] == "onedrive":
            remote_data["text"] = "OneDrive album"
        else:
            remote_data["text"] = "shared album"

    # Setup the jinja2 environment
    file_loader = jinja2.FileSystemLoader(gallery_config["templates_path"])
    env = jinja2.Environment(loader=file_loader)

    # Renter the HTML template
    template = env.get_template("index_template.jinja")
    html = template.render(
        images=images_data_list,
        gallery_config=gallery_config,
        background_photo=background_photo,
        remote_data=remote_data,
    )

    with open(
        os.path.join(gallery_config["public_path"], "index.html"), "w", encoding="utf-8"
    ) as out:
        out.write(html)


def main():
    """
    Builds the HTML gallery, generating all required files for display (thumbnails, images_data.json and index.html).
    """

    # Parse the arguments
    args = parse_args()

    # Read the gallery config
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    if not gallery_config:
        spg_common.log(f"Cannot load the gallery.json file ({gallery_config_path})!")
        sys.exit(1)

    spg_common.log("Building the Simple Photo Gallery...")

    # Get the gallery logic
    gallery_logic = get_gallery_logic(gallery_config)

    # Check if thumbnails exist and generate them if needed or if specified by the user
    try:
        spg_common.log("Generating thumbnails...")
        gallery_logic.create_thumbnails(args.force_thumbnails)
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the thumbnails: {str(exception)}"
        )
        sys.exit(1)

    # Generate the images_data.json
    try:
        spg_common.log("Generating the images_data.json file...")
        gallery_logic.create_images_data_file()
        spg_common.log(
            "The image descriptions are stored in images_data.json. You can edit the file to add more "
            "descriptions and build the gallery again."
        )
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the images_data.json file: {str(exception)}"
        )
        sys.exit(1)

    # Build the HTML from the templates
    try:
        spg_common.log("Creating the index.html...")
        build_html(gallery_config)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the gallery HTML: {str(exception)}"
        )
        sys.exit(1)

    spg_common.log(
        "The gallery was built successfully. Open public/index.html to view it."
    )


if __name__ == "__main__":
    main()
