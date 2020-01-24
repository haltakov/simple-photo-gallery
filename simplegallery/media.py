import glob
import cv2
import os
from PIL import Image, ExifTags
import simplegallery.common as spg_common


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
