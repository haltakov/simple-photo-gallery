import unittest
import simplegallery.common as spg_common
from simplegallery.upload.uploader_factory import get_uploader
from simplegallery.upload.variants.aws_uploader import AWSUploader
from simplegallery.upload.variants.netlify_uploader import NetlifyUploader


class UploaderFactoryTestCase(unittest.TestCase):
    def test_get_uploader(self):
        self.assertIs(AWSUploader, get_uploader("aws").__class__)
        self.assertIs(NetlifyUploader, get_uploader("netlify").__class__)

        with self.assertRaises(spg_common.SPGException):
            get_uploader("non_existing_uploader")


if __name__ == "__main__":
    unittest.main()
