import unittest
from unittest import mock
import os
import subprocess
from testfixtures import TempDirectory
from simplegallery.upload.uploader_factory import get_uploader


class NetlifyUploaderTestCase(unittest.TestCase):

    def test_netlify_without_location(self):
        uploader = get_uploader('netlify')
        self.assertTrue(uploader.check_location(''))

    @mock.patch('subprocess.run')
    def test_upload_gallery(self, subprocess_run):
        subprocess_run.return_value = subprocess.CompletedProcess([], returncode=0)

        with TempDirectory() as tempdir:
            # Setup mock file and uploader
            tempdir.write('index.html', b'')
            gallery_path = os.path.join(tempdir.path, 'index.html')
            uploader = get_uploader('netlify')

            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
