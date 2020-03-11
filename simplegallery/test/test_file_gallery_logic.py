import unittest
from unittest import mock
import sys
import os
import json
from PIL import Image
from testfixtures import TempDirectory
import simplegallery.gallery_init as gallery_init
import simplegallery.media as spg_media
from simplegallery.logic.files_gallery_logic import FilesGalleryLogic


def create_mock_image(path, width, height):
    img = Image.new('RGB', (width, height), color='red')
    img.save(path)
    img.close()


def init_gallery_and_read_gallery_config(tempdir):
    sys.argv = ['gallery_init', '-p', tempdir.path]
    gallery_init.main()

    with open(os.path.join(tempdir.path, 'gallery.json'), 'r') as json_in:
        gallery_config = json.load(json_in)

    return gallery_config


class FileGalleryLogicTestCase(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['', '', ''])
    def test_create_thumbnails(self, input):
        with TempDirectory() as tempdir:
            create_mock_image(os.path.join(tempdir.path, 'photo.jpg'), 1000, 500)

            thumbnail_path = os.path.join(tempdir.path, 'public', 'images', 'thumbnails', 'photo.jpg')

            # Init files gallery logic
            gallery_config = init_gallery_and_read_gallery_config(tempdir)
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            # Check no thumbnails exist
            tempdir.compare(['.empty'], path='public/images/thumbnails')

            # Check thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare(['.empty', 'photo.jpg'], path='public/images/thumbnails')
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail not regenerated without force
            create_mock_image(os.path.join(tempdir.path, 'public', 'images', 'photos', 'photo.jpg'), 500, 500)
            file_gallery_logic.create_thumbnails()
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail regenerated with force
            file_gallery_logic.create_thumbnails(force=True)
            self.assertEqual((320, 320), spg_media.get_image_size(thumbnail_path))

    def check_image_data(self, images_data, image_name, description, size, thumbnail_size):
        image_data = images_data[image_name]
        self.assertEqual(description, image_data['description'])
        self.assertTrue(image_data['mtime'])
        self.assertEqual(size, image_data['size'])
        self.assertEqual(os.path.join('images', 'photos', image_name), image_data['src'])
        self.assertEqual(os.path.join('images', 'thumbnails', image_name), image_data['thumbnail'])
        self.assertEqual(thumbnail_size, image_data['thumbnail_size'])
        self.assertEqual('image', image_data['type'])

    @mock.patch('builtins.input', side_effect=['', '', ''])
    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            create_mock_image(os.path.join(tempdir.path, 'photo.jpg'), 1000, 500)

            # Init files gallery logic
            gallery_config = init_gallery_and_read_gallery_config(tempdir)
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(1, len(images_data))
            self.check_image_data(images_data, 'photo.jpg', '', (1000, 500), (640, 320))

            # Change a description, add a new image and check description of the first is preserved
            images_data['photo.jpg']['description'] = 'Test description'
            create_mock_image(os.path.join(tempdir.path, 'public', 'images', 'photos', 'photo2.jpg'), 1000, 500)
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data(images_data)
            self.assertEqual(2, len(images_data))
            self.check_image_data(images_data, 'photo.jpg', 'Test description', (1000, 500), (640, 320))


if __name__ == '__main__':
    unittest.main()
