import argparse
import logging
import os
import simplegallery.common as spg_common
import simplegallery.media as spg_media
import sys
import glob


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Builds the HTML gallery, generating all required files for display.'''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-g', '--gallery',
                        dest='gallery_path',
                        action='store',
                        default=os.path.join('.', 'gallery.json'),
                        help='Path to the gallery.json file')

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

    photos = glob.glob(os.path.join(gallery_config['images_path'], '*'))

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


def main():
    # Init the logger
    spg_common.setup_gallery_logging()

    # Parse the arguments
    args = parse_args()

    # Read the gallery config
    gallery_config = spg_common.read_gallery_config(args.gallery_path)
    if not gallery_config:
        logging.error(f'Cannot load the gallery.json file ({args.gallery_path})!')
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


if __name__ == "__main__":
    main()

