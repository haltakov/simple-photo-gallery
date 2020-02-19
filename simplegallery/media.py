import glob
import os
import json
import cv2
from PIL import Image, ExifTags
import simplegallery.common as spg_common


# Mapping of the string representation if an Exif tag to its id
EXIF_TAG_MAP = {ExifTags.TAGS[tag]: tag for tag in ExifTags.TAGS}


def rotate_image_by_orientation(image):
    """
    Rotates an image according to it's Orientation EXIF Tag
    :param im: Image
    :return: Rotated image
    """

    exif = image._getexif()
    if exif and EXIF_TAG_MAP['Orientation'] in exif:
        orientation = exif[EXIF_TAG_MAP['Orientation']]

        if orientation == 3:
            rotation_angle = 180
        elif orientation == 6:
            rotation_angle = 270
        elif orientation == 8:
            rotation_angle = 90
        else:
            rotation_angle = 0

        if rotation_angle != 0:
            return image.rotate(rotation_angle, expand=True)

    return image


def create_image_thumbnail(image_path, thumbnail_path, height):
    """
    Creates a thumbnail for an image
    :param image_path: input image path
    :param thumbnail_path: path to the thumbnail file
    :param height: height of the thumbnail in pixels
    """
    image = Image.open(image_path)

    image = rotate_image_by_orientation(image)

    width = round((float(height)/image.size[1]) * image.size[0])
    image = image.resize((width, height), Image.ANTIALIAS)

    image.save(thumbnail_path)
    image.close()


def create_video_thumbnail(video_path, thumbnail_path, height):
    """
    Creates a thumbnail for a video out of the first video frame
    :param video_path: input video path
    :param thumbnail_path: path to the thumbnail file
    :param height: height of the thumbnail in pixels
    """
    video_capture = cv2.VideoCapture(video_path)
    _, image = video_capture.read()
    thumbnail = cv2.resize(image, (round(image.shape[1] * float(height)/image.shape[0]), height))
    cv2.imwrite(thumbnail_path, thumbnail)


def create_thumbnail(input_path, thumbnails_path, height):
    """
    Creates a thumbnail for a media file (image or video)
    :param input_path: input media path (image or video)
    :param thumbnails_path: path to the folder, where the thumbnail should be stored
    :param height: height of the thumbnail in pixels
    """
    # Handle JPGs and GIFs
    if input_path.lower().endswith('.jpg') or input_path.lower().endswith('.jpeg') or input_path.lower().endswith('.gif'):
        thumbnail_path = os.path.join(thumbnails_path, os.path.basename(input_path))
        create_image_thumbnail(input_path, thumbnail_path, height)
    # Handle MP4s
    elif input_path.lower().endswith('.mp4'):
        thumbnail_path = os.path.join(thumbnails_path, os.path.basename(input_path)).replace('.mp4', '.jpg').replace('.MP4', '.jpg')
        create_video_thumbnail(input_path, thumbnail_path, height)
    else:
        raise spg_common.SPGException(f'Unsupported file type ({os.path.basename(input_path)})')


def get_image_size(image_path):
    """
    Gets the size of an image in pixels
    :param image_path: Path to the image
    :return: tuple containing the width and the height of the image in pixels
    """
    image = Image.open(image_path)
    size = image.size
    image.close()

    return size


# Get the size of a video in pixels
def get_video_size(video):
    """
    Gets the size of a frame of a video in pixels
    :param video: Path to the video
    :return: tuple containing the width and the height of the frame in pixels
    """
    video_capture = cv2.VideoCapture(video)
    _, image = video_capture.read()
    return image.shape[1], image.shape[0]


# Get the image description from the EXIF data
def get_image_description(image_path):
    """
    Gets the description of an image from the ImageDescription tag as a utf-8 string
    :param image_path: Path to the image
    :return: String (utf-8) containing the image description
    """
    image = Image.open(image_path)
    exif = image._getexif()
    if exif and EXIF_TAG_MAP['ImageDescription'] in exif:
        description = exif[EXIF_TAG_MAP['ImageDescription']].encode(encoding='utf-16')[2::2].decode('utf-8')
        description = description.replace('\'', '&apos;').replace('"', '&quot;')
    else:
        description = ''

    image.close()

    return description


def get_metadata(image, thumbnail_path, public_path):
    """
    Gets the metadata of a media file (image or vieo)
    :param image: Path to the media fule
    :param thumbnail_path: Path to the thumbnail image of the media file
    :param public_path: Path to the public folder of the gallery
    :return:
    """
    # Paths should be relative to the public folder, because they will directly be used in the HTML
    image_data = dict(src=os.path.relpath(image, public_path),
                      mtime=os.path.getmtime(image))

    if image.lower().endswith('.jpg') or image.lower().endswith('.jpeg'):
        image_data['size'] = get_image_size(image)
        image_data['type'] = 'image'
        image_data['description'] = get_image_description(image)
    elif image.lower().endswith('.gif'):
        image_data['size'] = get_image_size(image)
        image_data['type'] = 'image'
        image_data['description'] = ''
    elif image.lower().endswith('.mp4'):
        image_data['size'] = get_video_size(image)
        image_data['type'] = 'video'
        image_data['description'] = ''
        thumbnail_path = thumbnail_path.replace('.mp4', '.jpg')
    else:
        raise spg_common.SPGException(f'Unsupported file type {os.path.basename(image)}')

    image_data['thumbnail'] = os.path.relpath(thumbnail_path, public_path)
    image_data['thumbnail_size'] = get_image_size(thumbnail_path)

    return image_data


def create_images_data_file(images_data_path, images_path, thumbnails_path, public_path):
    """
    Updates the images_data.json file for each new image to store metadata (like size, description and thumbnail)
    :param images_data_path: Path to the images_data.json file
    :param images_path: Path to the folder containing all images
    :param thumbnails_path: Path to the folder containing all thumbnails
    :param public_path: Path to the public folder of the gallery
    """

    # Get all images
    images = glob.glob(os.path.join(images_path, '*.*'))

    # Load the existing file or create an empty dict
    if os.path.exists(images_data_path):
        with open(images_data_path, 'r') as images_data_in:
            images_data = json.load(images_data_in)
    else:
        images_data = {}

    # Get the required metadata for each image
    for image in images:
        photo_name = os.path.basename(image)
        thumbnail_path = os.path.join(thumbnails_path, photo_name)

        image_data = get_metadata(image, thumbnail_path, public_path)

        # Check if the image file has changed and only then use the new metadata. This allows changes that were made to
        # the metadata (for example to the descriptions) to be preserved, unless the photo itself changed.

        if photo_name not in images_data or images_data[photo_name]['mtime'] != image_data['mtime']:
            images_data[photo_name] = image_data

    # Write the data to a JSON file
    with open(images_data_path, 'w', encoding='utf-8') as images_out:
        json.dump(images_data, images_out, indent=4, separators=(',', ': '), sort_keys=True)
