import glob
import cv2
import os
import json
from PIL import Image, ExifTags
import simplegallery.common as spg_common


# Mapping of the string representation if an Exif tag to its id
EXIF_TAG_MAP = {ExifTags.TAGS[tag]: tag for tag in ExifTags.TAGS}


def create_image_thumbnail(image_path, thumbnail_path, height):
    """
    Creates a thumbnail for an image
    :param image_path: input image path
    :param thumbnail_path: path to the thumbnail file
    :param height: height of the thumbnail in pixels
    """
    im = Image.open(image_path)
    width = round((float(height)/im.size[1]) * im.size[0])
    im = im.resize((width, height), Image.ANTIALIAS)
    im.save(thumbnail_path)
    im.close()


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


def get_image_size(image):
    """
    Gets the size of an image in pixels
    :param image: Path to the image
    :return: tuple containing the width and the height of the image in pixels
    """
    im = Image.open(image)
    size = im.size
    im.close()

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
def get_image_description(image):
    """
    Gets the description of an image from the ImageDescription tag as a utf-8 string
    :param image: Path to the image
    :return: String (utf-8) containing the image description
    """
    im = Image.open(image)
    exif = im._getexif()
    if exif and EXIF_TAG_MAP['ImageDescription'] in exif:
        description = exif[EXIF_TAG_MAP['ImageDescription'] ].encode(encoding='utf-16')[2::2].decode('utf-8')
        description = description.replace('\'', '&apos;').replace('"', '&quot;')
    else:
        description = ''

    return description


def create_images_data_file(images_path, thumbnails_path, images_data_path, public_path):
    """
    Creates the images_data.json file containing metadata for each image (including size, description and thumbnail)
    :param images_path: Path to the folder containing all images
    :param thumbnails_path: Path to the folder containing all thumbnails
    :param images_data_path: Path to the images_data.json file
    :param public_path: Path to the public folder of the gallery
    :param force: Forces the generation of the images_data.json file if set to true
    """

    # Get all images
    images = glob.glob(os.path.join(images_path, '*.*'))

    data = []
    # Get the required metadata for each image
    for image in sorted(images):
        thumbnail_path = os.path.join(thumbnails_path, os.path.basename(image))

        # Paths should be relative to the public folder, because they will directly be used in the HTML
        d = dict(src=os.path.relpath(image, public_path))

        if image.lower().endswith('.jpg') or image.lower().endswith('.jpeg'):
            d['size'] = get_image_size(image)
            d['type'] = 'image'
            d['description'] = get_image_description(image)
        elif image.lower().endswith('.gif'):
            d['size'] = get_image_size(image)
            d['type'] = 'image'
            d['description'] = ''
        elif image.lower().endswith('.mp4'):
            d['size'] = get_video_size(image)
            d['type'] = 'video'
            d['description'] = ''
            thumbnail_path = thumbnail_path.replace('.mp4', '.jpg')
        else:
            raise spg_common.SPGException(f'Unsupported file type {os.path.basename(image)}')

        d['thumbnail'] = os.path.relpath(thumbnail_path, public_path)
        d['thumbnail_size'] = get_image_size(thumbnail_path)

        data.append(d)

    # Write the data to a JSON file
    with open(images_data_path, 'w') as images_out:
        json.dump(data, images_out, indent=4, separators=(',', ': '))
