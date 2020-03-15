import os
import glob
import simplegallery.common as spg_common
import simplegallery.media as spg_media
from simplegallery.logic.base_gallery_logic import BaseGalleryLogic


class FilesGalleryLogic(BaseGalleryLogic):
    """
    Gallery logic for a gallery composed of photos and videos stored as local files.
    """

    def create_thumbnails(self, force=False):
        """
        Checks if every image has an existing thumbnail and generates it if not (or if forced by the user)
        :param force: Forces generation of thumbnails if set to true
        """

        thumbnails_path = self.gallery_config['thumbnails_path']
        thumbnails_height = self.gallery_config['thumbnail_height']

        photos = glob.glob(os.path.join(self.gallery_config['images_path'], '*.*'))

        if not photos:
            raise spg_common.SPGException(f'No photos could be found under {self.gallery_config["images_path"]}')

        count_thumbnails_created = 0
        for photo in photos:
            photo_name = os.path.basename(photo).split('.')[0]

            # Check if the corresponding thumbnail is missing or if forced by the user
            if force or len(glob.glob(os.path.join(thumbnails_path, photo_name + '.*'))) == 0:
                spg_media.create_thumbnail(photo, thumbnails_path, thumbnails_height)
                count_thumbnails_created += 1

        spg_common.log(f'New thumbnails generated: {count_thumbnails_created}')

    def generate_images_data(self, images_data):
        """
        Generates the metadata of each image file
        :param images_data: Images data dictionary containing the existing metadata of the images and which will be
        updated by this function
        :return updated images data dictionary
        """

        # Get all images
        images = glob.glob(os.path.join(self.gallery_config['images_path'], '*.*'))

        # Get the required metadata for each image
        for image in images:
            photo_name = os.path.basename(image)
            thumbnail_path = os.path.join(self.gallery_config['thumbnails_path'], photo_name)

            image_data = spg_media.get_metadata(image, thumbnail_path, self.gallery_config['public_path'])

            # Check if the image file has changed and only then use the new metadata. This allows changes that were made to
            # the metadata (for example to the descriptions) to be preserved, unless the photo itself changed.
            if photo_name not in images_data or images_data[photo_name]['mtime'] != image_data['mtime']:
                images_data[photo_name] = image_data

        return images_data



