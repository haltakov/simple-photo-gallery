import os
import cv2
import requests
from io import BytesIO
from PIL import Image, ExifTags
from datetime import datetime
import simplegallery.common as spg_common


# Mapping of the string representation if an Exif tag to its id
EXIF_TAG_MAP = {ExifTags.TAGS[tag]: tag for tag in ExifTags.TAGS}


def rotate_image_by_orientation(image):
    """
    Rotates an image according to it's Orientation EXIF Tag
    :param im: Image
    :return: Rotated image
    """

    try:
        exif = image._getexif()
        if exif and EXIF_TAG_MAP["Orientation"] in exif:
            orientation = exif[EXIF_TAG_MAP["Orientation"]]

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
    except:
        pass

    return image


def get_thumbnail_size(image_size, thumbnail_height):
    """
    Computes the size of a thumbnail
    :param image_size: original image size
    :param thumbnail_height: thumbnail height
    :return: thumbnail size tuple
    """
    width = round((float(thumbnail_height) / image_size[1]) * image_size[0])
    return width, thumbnail_height


def create_image_thumbnail(image_path, thumbnail_path, height):
    """
    Creates a thumbnail for an image
    :param image_path: input image path
    :param thumbnail_path: path to the thumbnail file
    :param height: height of the thumbnail in pixels
    """
    image = Image.open(image_path)

    # Only rotate JPEGs, because they have the orientation in their metadata
    if image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
        image = rotate_image_by_orientation(image)

    thumbnail_size = get_thumbnail_size(image.size, height)
    image = image.resize(thumbnail_size, Image.ANTIALIAS)

    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")

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
    thumbnail = cv2.resize(
        image, (round(image.shape[1] * float(height) / image.shape[0]), height)
    )
    cv2.imwrite(thumbnail_path, thumbnail)


def create_thumbnail(input_path, thumbnail_path, height):
    """
    Creates a thumbnail for a media file (image or video)
    :param input_path: input media path (image or video)
    :param thumbnail_path: path to the thumbnail file to be created
    :param height: height of the thumbnail in pixels
    """
    # Handle JPGs and GIFs
    if (
        input_path.lower().endswith(".jpg")
        or input_path.lower().endswith(".jpeg")
        or input_path.lower().endswith(".gif")
        or input_path.lower().endswith(".png")
    ):
        create_image_thumbnail(input_path, thumbnail_path, height)
    # Handle MP4s
    elif input_path.lower().endswith(".mp4"):
        create_video_thumbnail(input_path, thumbnail_path, height)
    else:
        raise spg_common.SPGException(
            f"Unsupported file type ({os.path.basename(input_path)})"
        )


def get_remote_image_size(image_url):
    """
    Get the size of a remote image in pixels
    :param
    :return: tuple containing the width and the height of the image in pixels
    """
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    size = image.size
    image.close()

    return size


def get_image_size(image_path):
    """
    Gets the size of an image in pixels
    :param image_path: Path to the image
    :return: tuple containing the width and the height of the image in pixels
    """
    image = Image.open(image_path)
    image = rotate_image_by_orientation(image)
    size = image.size
    image.close()

    return size


def get_video_size(video):
    """
    Gets the size of a frame of a video in pixels
    :param video: Path to the video
    :return: tuple containing the width and the height of the frame in pixels
    """
    video_capture = cv2.VideoCapture(video)
    _, image = video_capture.read()
    return image.shape[1], image.shape[0]


def get_image_description(image_path):
    """
    Gets the description of an image from the ImageDescription tag as a utf-8 string
    :param image_path: Path to the image
    :return: String (utf-8) containing the image description
    """
    image = Image.open(image_path)
    exif = image._getexif()
    if exif and EXIF_TAG_MAP["ImageDescription"] in exif:
        description = (
            exif[EXIF_TAG_MAP["ImageDescription"]]
            .encode(encoding="utf-16")[2::2]
            .decode("utf-8")
        )
        description = description.replace("'", "&apos;").replace('"', "&quot;")
    else:
        description = ""

    image.close()

    return description


def parse_exif_datetime(timestamp_string):
    """
    Parses a date and time string as contained in the EXIF data of an image
    :param date_string: Date and time string
    :return:
    """
    timestamp_string = timestamp_string.split("+")[0]
    try:
        timestamp = datetime.strptime(timestamp_string, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        timestamp = None

    return timestamp


def get_image_date(image_path):
    """
    Gets the date at which the image was taken from the EXIF data or from the creation date of the file
    :param image_path: Path to the image
    :return: The date the image was taken
    """
    image_date = None

    if image_path.lower().endswith(".jpeg") or image_path.lower().endswith(".jpg"):
        image = Image.open(image_path)
        exif = image._getexif()
        image.close()

        if exif:
            if EXIF_TAG_MAP["DateTimeOriginal"] in exif:
                image_date = parse_exif_datetime(exif[EXIF_TAG_MAP["DateTimeOriginal"]])
            elif EXIF_TAG_MAP["DateTimeDigitized"] in exif:
                image_date = parse_exif_datetime(
                    exif[EXIF_TAG_MAP["DateTimeDigitized"]]
                )
            elif EXIF_TAG_MAP["DateTime"] in exif:
                image_date = parse_exif_datetime(exif[EXIF_TAG_MAP["DateTime"]])

    if not image_date:
        image_date = datetime.fromtimestamp(os.path.getctime(image_path))

    return image_date


def get_metadata(image, thumbnail_path, public_path):
    """
    Gets the metadata of a media file (image or video)
    :param image: Path to the media file
    :param thumbnail_path: Path to the thumbnail image of the media file
    :param public_path: Path to the public folder of the gallery
    :return:
    """
    # Paths should be relative to the public folder, because they will directly be used in the HTML
    image_data = dict(
        src=os.path.relpath(image, public_path),
        mtime=os.path.getmtime(image),
        date=get_image_date(image),
    )

    if image.lower().endswith(".jpg") or image.lower().endswith(".jpeg"):
        image_data["size"] = get_image_size(image)
        image_data["type"] = "image"
        image_data["description"] = get_image_description(image)
    elif image.lower().endswith(".gif") or image.lower().endswith(".png"):
        image_data["size"] = get_image_size(image)
        image_data["type"] = "image"
        image_data["description"] = ""
    elif image.lower().endswith(".mp4"):
        image_data["size"] = get_video_size(image)
        image_data["type"] = "video"
        image_data["description"] = ""
        thumbnail_path = thumbnail_path.replace(".mp4", ".jpg")
    else:
        raise spg_common.SPGException(
            f"Unsupported file type {os.path.basename(image)}"
        )

    image_data["thumbnail"] = os.path.relpath(thumbnail_path, public_path)
    image_data["thumbnail_size"] = get_image_size(thumbnail_path)

    return image_data
