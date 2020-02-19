import argparse
import os
import sys
import glob
import json
from collections import OrderedDict
import jinja2
import simplegallery.common as spg_common
import simplegallery.media as spg_media


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Generated all files needed to display the gallery (thumbnails, image descriptions and HTML page).
                    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery.'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-p', '--path',
                        dest='path',
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

    spg_common.log(f'New thumbnails generated: {count_thumbnails_created}')


def build_html(gallery_config):
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

    with open(os.path.join(gallery_config['public_path'], 'index.html'), 'w', encoding='utf-8') as out:
        out.write(html)


def main():
    """
    Builds the HTML gallery, generating all required files for display (thumbnails, images_data.json and index.html).
    """

    # Parse the arguments
    args = parse_args()

    # Read the gallery config
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, 'gallery.json')
    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    if not gallery_config:
        spg_common.log(f'Cannot load the gallery.json file ({gallery_config_path})!')
        sys.exit(1)

    spg_common.log('Building the Simple Photo Gallery...')

    # Check if thumbnails exist and generate them if needed or if specified by the user
    try:
        spg_common.log('Generating thumbnails...')
        check_and_create_thumbnails(gallery_config, args.force_thumbnails)
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(f'Something went wrong while generating the thumbnails: {str(exception)}')
        sys.exit(1)

    # Generate the images_data.json
    try:
        spg_common.log('Generating the images_data.json file...')
        spg_media.create_images_data_file(gallery_config['images_data_file'],
                                          gallery_config['images_path'],
                                          gallery_config['thumbnails_path'],
                                          gallery_config['public_path'])
        spg_common.log('The image descriptions are stored in images_data.json. You can edit the file to add more '
                       'descriptions and build the gallery again.')
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(f'Something went wrong while generating the images_data.json file: {str(exception)}')
        sys.exit(1)

    # Build the HTML from the templates
    try:
        spg_common.log('Creating the index.html...')
        build_html(gallery_config)
    except Exception as exception:
        spg_common.log(f'Something went wrong while generating the gallery HTML: {str(exception)}')
        sys.exit(1)

    spg_common.log('The gallery was built successfully. Open public/index.html to view it.')


if __name__ == "__main__":
    main()
