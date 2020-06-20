import simplegallery.common as spg_common
from simplegallery.upload.variants.aws_uploader import AWSUploader
from simplegallery.upload.variants.netlify_uploader import NetlifyUploader


def get_uploader(hosting_type):
    """
    Factory function that returns an object of a class derived from BaseUploader based on the provided hosting type.
    Supported uploaders:
    - AWSUploader - uploader for AWS S3
    - Netlify - uploader for Netlify

    :param hosting_type: name of the hosting provider (aws or netlify)
    :return: uploader object
    """
    if hosting_type == "aws":
        return AWSUploader()
    elif hosting_type == "netlify":
        return NetlifyUploader()
    else:
        raise spg_common.SPGException(f"Hosting type not supported: {hosting_type}")
