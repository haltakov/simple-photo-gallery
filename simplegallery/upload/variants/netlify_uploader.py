import subprocess
import simplegallery.common as spg_common
from simplegallery.upload.base_uploader import BaseUploader


class NetlifyUploader(BaseUploader):

    def check_location(self, location):
        return True

    def upload_gallery(self, location, gallery_path):
        pass

