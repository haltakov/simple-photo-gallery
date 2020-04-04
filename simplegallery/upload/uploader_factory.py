import simplegallery.common as spg_common
from simplegallery.upload.variants.aws_uploader import AWSUploader
from simplegallery.upload.variants.netlify_uploader import NetlifyUploader


def get_uploader(hosting_type):
    if hosting_type == 'aws':
        return AWSUploader()
    elif hosting_type == 'netlify':
        return NetlifyUploader()
    else:
        raise spg_common.SPGException(f"Hosting type not supported: {hosting_type}")