import simplegallery.common as spg_common
from simplegallery.upload.variants.aws_uploader import AWSUploader


def get_uploader(hosting_type):
    if hosting_type == 'aws':
        return AWSUploader()
    else:
        raise spg_common.SPGException(f"Hosting type not supported: {hosting_type}")