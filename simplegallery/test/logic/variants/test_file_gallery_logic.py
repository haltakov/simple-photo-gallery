import unittest
from unittest import mock
import os
from testfixtures import TempDirectory
import simplegallery.test.helpers as helpers
import simplegallery.media as spg_media
from simplegallery.logic.variants.files_gallery_logic import FilesGalleryLogic


class FileGalleryLogicTestCase(unittest.TestCase):
    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_create_thumbnails(self, input):
        with TempDirectory() as tempdir:
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo.jpg"), 1000, 500
            )
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo2.gif"), 1000, 500
            )
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo3.png"), 1000, 500
            )

            thumbnail_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo.jpg"
            )
            thumbnail_gif_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo2.jpg"
            )
            thumbnail_png_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo3.jpg"
            )

            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(tempdir.path)
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            # Check no thumbnails exist
            tempdir.compare([".empty"], path="public/images/thumbnails")

            # Check thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare(
                [".empty", "photo.jpg", "photo2.jpg", "photo3.jpg"],
                path="public/images/thumbnails",
            )
            # The thumbnails are generated twice as big in order to improve the quality on retina displays
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_path))
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_gif_path))
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_png_path))

            # Check thumbnail not regenerated without force
            helpers.create_mock_image(
                os.path.join(tempdir.path, "public", "images", "photos", "photo.jpg"),
                500,
                500,
            )
            file_gallery_logic.create_thumbnails()
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail regenerated with force
            file_gallery_logic.create_thumbnails(force=True)
            self.assertEqual((320, 320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail regenerated after size changed
            gallery_config["thumbnail_height"] = 320
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            file_gallery_logic.create_thumbnails()
            self.assertEqual((640, 640), spg_media.get_image_size(thumbnail_path))

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo.jpg"), 1000, 500
            )

            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(tempdir.path)
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(1, len(images_data))
            helpers.check_image_data(
                self,
                images_data,
                "photo.jpg",
                "",
                (1000, 500),
                (320, 160),
                local_files=True,
            )

            # Change a description, add a new image and check description of the first is preserved
            images_data["photo.jpg"]["description"] = "Test description"
            helpers.create_mock_image(
                os.path.join(tempdir.path, "public", "images", "photos", "photo2.jpg"),
                1000,
                500,
            )
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data(images_data)
            self.assertEqual(2, len(images_data))
            helpers.check_image_data(
                self,
                images_data,
                "photo.jpg",
                "Test description",
                (1000, 500),
                (320, 160),
                local_files=True,
            )


if __name__ == "__main__":
    unittest.main()
