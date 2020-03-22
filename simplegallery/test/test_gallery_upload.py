import unittest
from unittest import mock
import sys
import os
import json
import subprocess
from PIL import Image
from testfixtures import TempDirectory
import simplegallery.gallery_init as gallery_init
import simplegallery.gallery_build as gallery_build
import simplegallery.gallery_upload as gallery_upload


def create_mock_image(path, width, height):
    img = Image.new('RGB', (width, height), color='red')
    img.save(path)
    img.close()


class SPGUploadTestCase(unittest.TestCase):

    def test_aws_without_location(self):
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['gallery_upload', 'aws']
            gallery_upload.main()

        self.assertEqual(cm.exception.code, 1)

    def test_gallery_not_initialized(self):
        with TempDirectory() as tempdir:
            with self.assertRaises(SystemExit) as cm:
                sys.argv = ['gallery_upload', 'aws', 'testbucket/path', '-p', tempdir.path]
                gallery_upload.main()

            self.assertEqual(cm.exception.code, 1)

    @mock.patch('builtins.input', side_effect=['', '', ''])
    def test_gallery_not_built(self, input):
        with TempDirectory() as tempdir:
            sys.argv = ['gallery_init', '-p', tempdir.path]
            gallery_init.main()

            with self.assertRaises(SystemExit) as cm:
                sys.argv = ['gallery_upload', 'aws', 'testbucket/path', '-p', tempdir.path]
                gallery_upload.main()

            self.assertEqual(cm.exception.code, 1)

    @mock.patch('builtins.input', side_effect=['', '', ''])
    @mock.patch('subprocess.run')
    def test_upload_aws(self, subprocess_run, input):
        subprocess_run.return_value = subprocess.CompletedProcess([], returncode=0)

        with TempDirectory() as tempdir:
            # Create a mock image
            create_mock_image(os.path.join(tempdir.path, 'photo.jpg'), 1000, 500)

            # Init and build the gallery
            public_path = os.path.join(tempdir.path, 'public')
            sys.argv = ['gallery_init', '-p', tempdir.path]
            gallery_init.main()
            sys.argv = ['gallery_build', '-p', tempdir.path]
            gallery_build.main()

            # Call upload without specified AWS S3 bucket
            with self.assertRaises(SystemExit) as cm:
                sys.argv = ['gallery_upload', 'aws', '-p', tempdir.path]
                gallery_upload.main()
            self.assertEqual(cm.exception.code, 1)

            # Call upload with a bucket specified as a parameter
            sys.argv = ['gallery_upload', 'aws', 's3://testbucket/path/', '-p', tempdir.path]
            gallery_upload.main()
            subprocess_run.assert_called_with(
                ['aws', 's3', 'sync', public_path, 's3://testbucket/path/', '--exclude', '.DS_Store'])

            # Call upload with a bucket specified in the gallery.json
            with open(os.path.join(tempdir.path, 'gallery.json'), 'r') as gallery_json_file:
                gallery_config = json.load(gallery_json_file)

            gallery_config['aws_location'] = 's3://testbucket/path/'

            with open(os.path.join(tempdir.path, 'gallery.json'), 'w') as gallery_json_file:
                json.dump(gallery_config, gallery_json_file)

            sys.argv = ['gallery_upload', 'aws', '-p', tempdir.path]
            gallery_upload.main()
            subprocess_run.ass
            subprocess_run.assert_called_with(['aws', 's3', 'sync', public_path, 's3://testbucket/path/', '--exclude', '.DS_Store'])

    def test_upload_netlify(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
