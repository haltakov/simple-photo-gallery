import os
import unittest
from unittest import mock
from testfixtures import TempDirectory
import simplegallery.test.helpers as helpers
from simplegallery.logic.variants.google_gallery_logic import GoogleGalleryLogic


class GoogleGalleryTestCase(unittest.TestCase):

    remote_link = "https://photos.app.goo.gl/cevaz94hQiF8Z5p67"

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_create_thumbnails(self, input):
        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(
                tempdir.path, self.remote_link
            )
            file_gallery_logic = GoogleGalleryLogic(gallery_config)

            # Check no thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare([".empty"], path="public/images/thumbnails")

    @unittest.skipUnless(
        "RUN_LONG_TESTS" in os.environ,
        "Long test - it involves downloading files from Google.",
    )
    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(
                tempdir.path, self.remote_link
            )
            file_gallery_logic = GoogleGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(2, len(images_data))
            helpers.check_image_data(
                self,
                images_data,
                "tGPJDmxLbrr9BTX_IHjh_MH1gJ7JhlcBnMBXPgWQslNLQSUjKGFdYd3TqTqTsGsYkpOJakSgcB05yB9aZJQ03JvRxHRLC0R0W4pYfbV2hXPlAgLHxIy1izHbhdWtrj4izcGbax6Pqw",
                "",
                (800, 600),
                (213, 160),
            )
            helpers.check_image_data(
                self,
                images_data,
                "lOHX7xeJqCo_lqxKBobKGjwFTW8qPMPCbaAKeqS3baU-VT_SPC0HrapdAEXFzkL98dAb9nCjlRhnmCSLoz520E1fZ-xuNPXAwXvM2PapP6uolH6rZsR3QKivxr_rtVADKuWVm2lz8Q",
                "",
                (1000, 1000),
                (160, 160),
            )


if __name__ == "__main__":
    unittest.main()
