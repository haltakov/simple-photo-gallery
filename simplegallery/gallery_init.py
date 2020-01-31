import argparse
import logging
import os
import sys
import pkg_resources
import glob
import shutil
import json
from distutils.dir_util import copy_tree
import simplegallery.common as spg_common


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Initializes a new Simple Photo Gallery in the specified folder (default is the current folder). 
    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-p', '--path',
                        dest='path',
                        action='store',
                        default='.',
                        help='Path to the folder which will be turned into a gallery')

    parser.add_argument('--force',
                        dest='force',
                        action='store_true',
                        help='Overrides existing config and template files files')

    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Enables verbose output')

    parser.add_argument('--keep-gallery-config',
                        dest='keep_gallery_config',
                        action='store_true',
                        help='Use to copy the template files only, without generating a gallery.json')

    return parser.parse_args()


def check_if_gallery_creation_possible(gallery_root):
    """
    Checks if a gallery can be created in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a new gallery can be created and false otherwise
    """

    # Check if the path exists
    if not os.path.exists(gallery_root):
        spg_common.log(f'The specified gallery path does not exist: {gallery_root}.')
        return False

    return True


def check_if_gallery_already_exists(gallery_root):
    """
    Checks if a gallery already exists in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a gallery exists and false otherwise
    """

    paths_to_check = [
        os.path.join(gallery_root, 'gallery.json'),
        os.path.join(gallery_root, 'images_data.json'),
        os.path.join(gallery_root, 'templates'),
        os.path.join(gallery_root, 'public'),
    ]

    # Check if any of the paths exists
    for path in paths_to_check:
        if os.path.exists(path):
            return True

    return False


def create_gallery_folder_structure(gallery_root):
    """
    Creates the gallery folder structure by copying all the gallery templates and moving all images and videos to the
    photos subfolder
    :param gallery_root: Path to the gallery root
    """

    # Copy the public and templates folder
    spg_common.log('Copying gallery template files...')
    copy_tree(pkg_resources.resource_filename('simplegallery', 'data/templates'), os.path.join(gallery_root, 'templates'))
    copy_tree(pkg_resources.resource_filename('simplegallery', 'data/public'), os.path.join(gallery_root, 'public'))

    # Move all images and videos to the correct subfolder under public
    photos_dir = os.path.join(gallery_root, 'public', 'images', 'photos')
    spg_common.log(f'Moving all photos and videos to {photos_dir}...')

    for path in glob.glob(os.path.join(gallery_root, '*')):
        basename_lower = os.path.basename(path).lower()
        if basename_lower.endswith('.jpg') or basename_lower.endswith('.jpeg') or basename_lower.endswith('.gif') or basename_lower.endswith('.mp4'):
            shutil.move(path, os.path.join(photos_dir, os.path.basename(path)))


def create_gallery_json(gallery_root):
    """
    Creates a new gallery.json file, based on settings specified by the user
    :param gallery_root: Path to the gallery root
    """

    spg_common.log('Creating the gallery config...')
    spg_common.log('You can answer the following questions in order to set some important gallery properties. You can '
                   'also just press Enter to leave the default and change it later in the gallery.json file.')

    # Initialize the gallery config with the main gallery paths
    gallery_config = dict(
        images_data_file=os.path.join(gallery_root, 'images_data.json'),
        public_path=os.path.join(gallery_root, 'public'),
        templates_path=os.path.join(gallery_root, 'templates'),
        images_path=os.path.join(gallery_root, 'public', 'images', 'photos'),
        thumbnails_path=os.path.join(gallery_root, 'public', 'images', 'thumbnails'),
    )

    # Set configuration defaults
    DEFAULT_TITLE = 'My Gallery'
    DEFAULT_DESCRIPTION = 'Default description of my gallery'
    DEFAULT_THUMBNAIL_HEIGHT = '320'
    DEFAULT_BACKGROUND_OFFSET = '30'

    # Ask the user for the title
    gallery_config['title'] = input(f'What is the title of your gallery? (default: "{DEFAULT_TITLE}")\n') or DEFAULT_TITLE

    # Ask the user for the description
    gallery_config['description'] = input(f'What is the description of your gallery? (default: "{DEFAULT_DESCRIPTION}")\n') or DEFAULT_DESCRIPTION

    # Ask the user for the thumbnail size
    while True:
        thumbnail_size = input(f'What should be the height of your thumbnails (between 32 and 1024)? (default: {DEFAULT_THUMBNAIL_HEIGHT})\n') or DEFAULT_THUMBNAIL_HEIGHT
        if thumbnail_size.isdigit():
            thumbnail_size = int(thumbnail_size)
            if 32 <= thumbnail_size <= 1024:
                break
    gallery_config['thumbnail_height'] = thumbnail_size

    # Ask the user for the background image
    gallery_config['background_photo'] = input(f'Which image should be used as background for the header? (default: "")\n')

    # Ask the user for the background offset
    while True:
        background_offset = input(
            f'What should be the vertical offset of the background image in %? (default: {DEFAULT_BACKGROUND_OFFSET})\n') or DEFAULT_BACKGROUND_OFFSET
        if background_offset.isdigit():
            background_offset = int(background_offset)
            if 0 <= background_offset <= 100:
                break
    gallery_config['background_photo_offset'] = background_offset

    # Save the configuration to a file
    gallery_config_path = os.path.join(gallery_root, 'gallery.json')
    with open(gallery_config_path, 'w') as out:
        json.dump(gallery_config, out, indent=4, separators=(',', ': '))

    spg_common.log('Gallery config stored in gallery.json')


def main():
    """
    Initializes a new Simple Photo Gallery in a specified folder
    """
    # Init the logger
    spg_common.setup_gallery_logging()

    # Parse the arguments
    args = parse_args()

    # Get the gallery root from the arguments
    gallery_root = args.path

    # Check if a gallery can be created at this location
    if not check_if_gallery_creation_possible(gallery_root):
        sys.exit(1)

    # Check if the specified gallery root already contains a gallery
    if check_if_gallery_already_exists(gallery_root):
        if not args.force:
            spg_common.log('A Simple Photo Gallery already exists at the specified location. Set the --force parameter '
                           'if you want to overwrite it.')
            sys.exit(0)
        else:
            spg_common.log('A Simple Photo Gallery already exists at the specified location, but will be overwritten.')
    spg_common.log('Creating a Simple Photo Gallery...')

    # Copy the template files to the gallery root
    create_gallery_folder_structure(gallery_root)

    # Create the gallery json file
    if not args.keep_gallery_config:
        create_gallery_json(gallery_root)

    spg_common.log('Simple Photo Gallery initialized successfully!')


if __name__ == "__main__":
    main()
