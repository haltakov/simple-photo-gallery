import os
import glob
from datetime import datetime
import simplegallery.common as spg_common
import simplegallery.media as spg_media
from simplegallery.logic.base_gallery_logic import BaseGalleryLogic


def check_correct_thumbnail_size(thumbnail_path, expected_height):
    """
    Check if a thumbnail has the correct height
    :param thumbnail_path: Path to the thumbnail file
    :param expected_height: Expected height of the thumbnail in pixels
    :return: True if the height of the thumbnail equals the expected height, False otherwise
    """
    return expected_height == spg_media.get_image_size(thumbnail_path)[1]


def get_thumbnail_name(thumbnails_path, photo_name):
    """
    Generates the full path to a thumbnail file
    :param thumbnails_path: Path to the folders where the thumbnails will be stored
    :param photo_name: Name of the original photo
    :return: Full path to the thumbnail file
    """
    photo_name_without_extension = os.path.basename(photo_name).split(".")[0]
    return os.path.join(thumbnails_path, photo_name_without_extension + ".jpg")


class FilesGalleryLogic(BaseGalleryLogic):
    """
    Gallery logic for a gallery composed of photos and videos stored as local files.
    """

    """
    Factor by which the size of the generated thumbnail should be multiplied in comparison to the size in the HTML.
    This is useful to generate larger thumbnails so that they can be displayed in high-quality on retina displays. 
    """
    THUMBNAIL_SIZE_FACTOR = 2

    def create_thumbnails(self, force=False):
        """
        Checks if every image has an existing thumbnail and generates it if not (or if forced by the user)
        :param force: Forces generation of thumbnails if set to true
        """

        # Multiply the thumbnail size by the factor to generate larger thumbnails to improve quality on retina displays
        thumbnail_height = (
            self.gallery_config["thumbnail_height"]
            * FilesGalleryLogic.THUMBNAIL_SIZE_FACTOR
        )
        thumbnails_path = self.gallery_config["thumbnails_path"]

        photos = glob.glob(os.path.join(self.gallery_config["images_path"], "*.*"))

        if not photos:
            raise spg_common.SPGException(
                f'No photos could be found under {self.gallery_config["images_path"]}'
            )

        count_thumbnails_created = 0
        for photo in photos:
            thumbnail_path = get_thumbnail_name(thumbnails_path, photo)

            # Check if the thumbnail should be generated. This happens if one of the following applies:
            # - Forced by the user with -f
            # - No thumbnail for this image
            # - The thumbnail image size doesn't correspond to the specified size
            if (
                force
                or not os.path.exists(thumbnail_path)
                or not check_correct_thumbnail_size(thumbnail_path, thumbnail_height)
            ):
                spg_media.create_thumbnail(photo, thumbnail_path, thumbnail_height)
                count_thumbnails_created += 1

        spg_common.log(f"New thumbnails generated: {count_thumbnails_created}")

    def format_image_date(self, timestamp):
        """
        Formats an image date according to the format specified in the gallery config.
        If no format is specified an empty string is returned
        :param timestamp: datetime object
        :return: Image date string or an empty string
        """
        image_date_string = ""

        if "date_format" in self.gallery_config:
            try:
                image_date_string = timestamp.strftime(
                    self.gallery_config["date_format"]
                )
            except ValueError:
                pass

        return image_date_string

    def generate_images_data(self, images_data):
        """
        Generates the metadata of each image file
        :param images_data: Images data dictionary containing the existing metadata of the images and which will be
        updated by this function
        :return updated images data dictionary
        """

        # Get all images sorted by name
        images = sorted(
            glob.glob(os.path.join(self.gallery_config["images_path"], "*.*"))
        )

        # Get the required metadata for each image
        for image in images:
            photo_name = os.path.basename(image)

            thumbnail_path = get_thumbnail_name(
                self.gallery_config["thumbnails_path"], image
            )
            image_data = spg_media.get_metadata(
                image, thumbnail_path, self.gallery_config["public_path"]
            )

            # Scale down the thumbnail size to the display size
            image_data["thumbnail_size"] = (
                round(
                    image_data["thumbnail_size"][0]
                    / FilesGalleryLogic.THUMBNAIL_SIZE_FACTOR
                ),
                round(
                    image_data["thumbnail_size"][1]
                    / FilesGalleryLogic.THUMBNAIL_SIZE_FACTOR
                ),
            )

            # Format the image date
            image_data["date"] = self.format_image_date(image_data["date"])

            # If the date is filled, set the description to a non-empty string so it is shown
            if image_data["date"] and not image_data["description"]:
                image_data["description"] = " "

            # Preserve the image description if the photo hasn't changed since the last time
            if (
                photo_name in images_data
                and images_data[photo_name]["mtime"] == image_data["mtime"]
                and images_data[photo_name]["description"]
            ):
                image_data["description"] = images_data[photo_name]["description"]

            images_data[photo_name] = image_data

        return images_data
