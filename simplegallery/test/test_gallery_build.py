import unittest
from unittest import mock
import sys
import os
import json
from PIL import Image
from testfixtures import TempDirectory
import simplegallery.gallery_init as gallery_init
import simplegallery.gallery_build as gallery_build
import simplegallery.media as spg_media


def create_mock_image(path, width, height):
    img = Image.new("RGB", (width, height), color="red")
    img.save(path)
    img.close()


class SPGBuildTestCase(unittest.TestCase):
    def test_nonexisting_gallery_config(self):
        with TempDirectory() as tempdir:
            with self.assertRaises(SystemExit) as cm:
                sys.argv = ["gallery_build", "-p", tempdir.path]
                gallery_build.main()

            self.assertEqual(cm.exception.code, 1)

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_thumbnails_generation(self, input):
        with TempDirectory() as tempdir:
            create_mock_image(os.path.join(tempdir.path, "photo.jpg"), 1000, 500)

            thumbnail_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo.jpg"
            )

            sys.argv = ["gallery_init", "-p", tempdir.path]
            gallery_init.main()

            # Check no thumbnails exist
            tempdir.compare([".empty"], path="public/images/thumbnails")

            # Check thumbnail created
            sys.argv = ["gallery_build", "-p", tempdir.path]
            gallery_build.main()
            tempdir.compare([".empty", "photo.jpg"], path="public/images/thumbnails")
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail not regenerated without force
            create_mock_image(
                os.path.join(tempdir.path, "public", "images", "photos", "photo.jpg"),
                500,
                500,
            )
            sys.argv = ["gallery_build", "-p", tempdir.path]
            gallery_build.main()
            self.assertEqual((640, 320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail regenerated with force
            sys.argv = ["gallery_build", "-p", tempdir.path, "-ft"]
            gallery_build.main()
            self.assertEqual((320, 320), spg_media.get_image_size(thumbnail_path))

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_images_data_generation(self, input):
        with TempDirectory() as tempdir:
            create_mock_image(os.path.join(tempdir.path, "photo.jpg"), 1000, 500)

            sys.argv = ["gallery_init", "-p", tempdir.path]
            gallery_init.main()

            sys.argv = ["gallery_build", "-p", tempdir.path]
            gallery_build.main()

            tempdir.compare(
                ["templates", "public", "gallery.json", "images_data.json"],
                recursive=False,
            )

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_index_html(self, input):
        with TempDirectory() as tempdir:
            create_mock_image(os.path.join(tempdir.path, "photo.jpg"), 1000, 500)

            sys.argv = ["gallery_init", "-p", tempdir.path]
            gallery_init.main()

            sys.argv = ["gallery_build", "-p", tempdir.path]
            gallery_build.main()

            tempdir.compare(
                ["css", "images", "js", "index.html"], path="public", recursive=False
            )

            with open(
                os.path.join(tempdir.path, "public", "index.html"), "r"
            ) as html_in:
                html = html_in.read()

                self.assertIn("<title>My Gallery</title>", html)
                self.assertIn("<h1>My Gallery</h1>", html)
                self.assertIn(
                    '<div class="header-info-details">Default description of my gallery</div>',
                    html,
                )
                self.assertIn('<a href="images/photos/photo.jpg"', html)
                self.assertIn(
                    'background: #333366 url("images/photos/photo.jpg")', html
                )


if __name__ == "__main__":
    unittest.main()
