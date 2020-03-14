import unittest
from unittest import mock
import sys
import os
import json
from PIL import Image
from testfixtures import TempDirectory
import simplegallery.gallery_init as gallery_init
import simplegallery.media as spg_media
from simplegallery.logic.onedrive_gallery_logic import OnedriveGalleryLogic


REMOTE_LINK = 'https://1drv.ms/u/s!AkD5kF--59kUf28rkcQAphGO668?e=ELiTW6'


def init_gallery_and_read_gallery_config(tempdir, remote_link):
    sys.argv = ['gallery_init', remote_link, '-p', tempdir.path]
    gallery_init.main()

    with open(os.path.join(tempdir.path, 'gallery.json'), 'r') as json_in:
        gallery_config = json.load(json_in)

    return gallery_config


class OnedriveGalleryTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['', '', ''])
    def test_create_thumbnails(self, input):
        with TempDirectory() as tempdir:
            thumbnail_path = os.path.join(tempdir.path, 'public', 'images', 'thumbnails', 'photo.jpg')

            # Init files gallery logic
            gallery_config = init_gallery_and_read_gallery_config(tempdir, REMOTE_LINK)
            file_gallery_logic = OnedriveGalleryLogic(gallery_config)

            # Check no thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare(['.empty'], path='public/images/thumbnails')

    def check_image_data(self, images_data, image_name, description, size, thumbnail_size):
        image_data = images_data[image_name]
        self.assertEqual(description, image_data['description'])
        self.assertTrue(image_data['mtime'])
        self.assertEqual(size, image_data['size'])
        self.assertTrue(image_name in image_data['src'])
        self.assertTrue(image_name in image_data['thumbnail'])
        self.assertEqual(thumbnail_size, image_data['thumbnail_size'])
        self.assertEqual('image', image_data['type'])

    @unittest.skipUnless('RUN_LONG_TESTS' in os.environ, 'Long test - it involves downloading files from OneDrive.')
    @mock.patch('builtins.input', side_effect=['', '', ''])
    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = init_gallery_and_read_gallery_config(tempdir, REMOTE_LINK)
            file_gallery_logic = OnedriveGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(2, len(images_data))
            self.check_image_data(
                images_data,
                'image1.jpg',
                '',
                (800, 600),
                (427, 320),
            )
            self.check_image_data(
                images_data,
                'image2.jpg',
                '',
                (1000, 1000),
                (320, 320),
            )


if __name__ == '__main__':
    unittest.main()
