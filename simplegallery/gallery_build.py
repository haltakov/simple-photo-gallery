import argparse
import logging
import os
import simplegallery.common as spg_common
import simplegallery.media as spg_media
import sys
import glob
import jinja2
import json
from collections import OrderedDict


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Builds the HTML gallery, generating all required files for display.'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-g', '--gallery-root',
                        dest='gallery_root',
                        action='store',
                        default='.',
                        help='Path to the folder containing the gallery.json file')

    parser.add_argument('-ft', '--force-thumbnails',
                        dest='force_thumbnails',
                        action='store_true',
                        help='Forces the generation of the thumbnails even if they already exist')

    return parser.parse_args()


def check_and_create_thumbnails(gallery_config, force=False):
    """
    Checks if every image has an existing thumbnail and generates it if not (or if forced by the user)
    :param gallery_config: gallery configuration dictionary
    :param force: Forces generation of thumbnails if set to true
    :return the number of thumbnails that were created
    """

    thumbnails_path = gallery_config['thumbnails_path']
    thumbnails_height = gallery_config['thumbnail_height']

    photos = glob.glob(os.path.join(gallery_config['images_path'], '*.*'))

    if not photos:
        raise spg_common.SPGException(f'No photos could be found under {gallery_config["images_path"]}')

    count_thumbnails_created = 0
    for photo in photos:
        photo_name = os.path.basename(photo).split('.')[0]

        # Check if the corresponding thumbnail is missing or if forced by the user
        if force or len(glob.glob(os.path.join(thumbnails_path, photo_name + '.*'))) == 0:
            spg_media.create_thumbnail(photo, thumbnails_path, thumbnails_height)
            count_thumbnails_created += 1

    return count_thumbnails_created


def build_html(gallery_root, gallery_config):
    """
    Generates the HTML file (index.html) of the gallery
    :param gallery_config: Gallery configuration dictionary
    """

    # Load the images_data
    with open(gallery_config['images_data_file'], 'r') as images_data_in:
        images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)

    images_data_list = [images_data[image] for image in images_data.keys()]

    # Setup the jinja2 environment
    file_loader = jinja2.FileSystemLoader(gallery_config['templates_path'])
    env = jinja2.Environment(loader=file_loader)

    # Renter the HTML template
    template = env.get_template('index_template.jinja')
    html = template.render(images=images_data_list, gallery_config=gallery_config)

    with open(os.path.join(gallery_config['public_path'], 'index.html'), 'w') as out:
        out.write(html)
        logging.info('Generated index.html')


def main():
    """
    Builds the HTML gallery, generating all required files for display.
    """

    # Init the logger
    spg_common.setup_gallery_logging()

    # Parse the arguments
    args = parse_args()

    # Read the gallery config
    gallery_root = args.gallery_root
    gallery_config = spg_common.read_gallery_config(os.path.join(gallery_root, 'gallery.json'))
    if not gallery_config:
        logging.error(f'Cannot load the gallery.json file ({args.gallery_root})!')
        sys.exit(1)

    # Check if thumbnails exist and generate them if needed or if specified by the user
    try:
        count = check_and_create_thumbnails(gallery_config, args.force_thumbnails)
        logging.info(f'New thumbnails created: {count}')
    except spg_common.SPGException as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        logging.error(f'Something went wrong while generating the thumbnails: {str(e)}')
        sys.exit(1)

    # Generate the images_data.json
    logging.info('Generating the images_data.json file')
    try:
        spg_media.create_images_data_file(gallery_config['images_data_file'],
                                          gallery_config['images_path'],
                                          gallery_config['thumbnails_path'],
                                          gallery_config['public_path'])
    except spg_common.SPGException as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        logging.error(f'Something went wrong while generating the images_data.json file: {str(e)}')
        sys.exit(1)

    # Build the HTML from the templates
    try:
        build_html(gallery_root, gallery_config)
    except Exception as e:
        logging.error(f'Something went wrong while generating the gallery HTML: {str(e)}')
        print(e.with_traceback())
        sys.exit(1)


if __name__ == "__main__":
    main()

