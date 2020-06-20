import unittest
from unittest import mock
import sys
import os
import json
from testfixtures import TempDirectory
import simplegallery.gallery_init as gallery_init


def check_gallery_files(tempdir, files_photos, files_other):
    tempdir.compare(
        ["templates", "public", "gallery.json"] + files_other, recursive=False
    )
    tempdir.compare(
        ["index_template.jinja", "gallery_macros.jinja"],
        path="templates",
        recursive=False,
    )
    tempdir.compare(["css", "images", "js"], path="public", recursive=False)
    tempdir.compare([".empty"] + files_photos, path="public/images/photos")


class SPGInitTestCase(unittest.TestCase):
    def test_nonexisting_gallery_path(self):
        with TempDirectory() as tempdir:
            with self.assertRaises(SystemExit) as cm:
                sys.argv = [
                    "gallery_init",
                    "-p",
                    os.path.join(tempdir.path, "non_existing_path"),
                ]
                gallery_init.main()

            self.assertEqual(cm.exception.code, 1)

    def test_existing_gallery_no_force(self):
        with TempDirectory() as tempdir:
            tempdir.write("gallery.json", b"")

            with self.assertRaises(SystemExit) as cm:
                sys.argv = ["gallery_init", "-p", tempdir.path]
                gallery_init.main()

            self.assertEqual(cm.exception.code, 0)
            tempdir.compare(["gallery.json"])

    def check_gallery_config(
        self,
        gallery_config_file,
        gallery_root,
        title,
        description,
        thumbnail_height,
        background_photo,
        url="",
        remote_type=None,
        remote_link=None,
    ):
        with open(gallery_config_file, "r") as json_in:
            gallery_config = json.load(json_in)

        self.assertEqual(
            gallery_config["images_data_file"],
            os.path.join(gallery_root, "images_data.json"),
        )
        self.assertEqual(
            gallery_config["public_path"], os.path.join(gallery_root, "public")
        )
        self.assertEqual(
            gallery_config["templates_path"], os.path.join(gallery_root, "templates")
        )
        self.assertEqual(
            gallery_config["images_path"],
            os.path.join(gallery_root, "public", "images", "photos"),
        )
        self.assertEqual(
            gallery_config["thumbnails_path"],
            os.path.join(gallery_root, "public", "images", "thumbnails"),
        )
        self.assertEqual(gallery_config["title"], title)
        self.assertEqual(gallery_config["description"], description)
        self.assertEqual(gallery_config["thumbnail_height"], thumbnail_height)
        self.assertEqual(gallery_config["background_photo"], background_photo)
        self.assertEqual(gallery_config["url"], url)
        self.assertEqual(gallery_config["background_photo_offset"], 30)

        if remote_type or remote_link:
            self.assertEqual(gallery_config["remote_gallery_type"], remote_type)
            self.assertEqual(gallery_config["remote_link"], remote_link)
        else:
            self.assertNotIn("remote_gallery_type", gallery_config)
            self.assertNotIn("remote_link", gallery_config)

    @mock.patch(
        "builtins.input",
        side_effect=["Test Gallery", "Test Description", "photo.jpg", "example.com"],
    )
    def test_new_gallery_created(self, input):
        files_photos = ["photo.jpg", "photo.jpeg", "photo.gif", "video.mp4"]
        files_other = ["something.txt"]

        with TempDirectory() as tempdir:
            for file in files_photos + files_other:
                tempdir.write(file, b"")

            sys.argv = ["gallery_init", "-p", tempdir.path]
            gallery_init.main()

            check_gallery_files(tempdir, files_photos, files_other)
            self.check_gallery_config(
                os.path.join(tempdir.path, "gallery.json"),
                tempdir.path,
                "Test Gallery",
                "Test Description",
                160,
                "photo.jpg",
                "example.com",
            )

    @mock.patch(
        "builtins.input",
        side_effect=["Test Gallery", "Test Description", "photo.jpg", "example.com"],
    )
    def test_existing_gallery_override(self, input):
        files_photos = ["photo.jpg", "photo.jpeg", "photo.gif", "video.mp4"]
        files_other = ["something.txt"]

        with TempDirectory() as tempdir:
            for file in files_photos + files_other:
                tempdir.write(file, b"")

            tempdir.write("gallery.json", b"")

            sys.argv = ["gallery_init", "-p", tempdir.path, "--force"]
            gallery_init.main()

            check_gallery_files(tempdir, files_photos, files_other)
            self.check_gallery_config(
                os.path.join(tempdir.path, "gallery.json"),
                tempdir.path,
                "Test Gallery",
                "Test Description",
                160,
                "photo.jpg",
                "example.com",
            )

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_default_gallery_config(self, input):
        with TempDirectory() as tempdir:
            sys.argv = ["gallery_init", "-p", tempdir.path]
            gallery_init.main()

            self.check_gallery_config(
                os.path.join(tempdir.path, "gallery.json"),
                tempdir.path,
                "My Gallery",
                "Default description of my gallery",
                160,
                "",
            )

    @mock.patch(
        "builtins.input",
        side_effect=["Test Gallery", "Test Description", "photo.jpg", "example.com"],
    )
    def test_new_onedrive_gallery_created(self, input):
        with TempDirectory() as tempdir:
            sys.argv = [
                "gallery_init",
                "https://onedrive.live.com/test",
                "-p",
                tempdir.path,
            ]
            gallery_init.main()

            check_gallery_files(tempdir, [], [])
            self.check_gallery_config(
                os.path.join(tempdir.path, "gallery.json"),
                tempdir.path,
                "Test Gallery",
                "Test Description",
                160,
                "photo.jpg",
                "example.com",
                "onedrive",
                "https://onedrive.live.com/test",
            )

    @mock.patch(
        "builtins.input",
        side_effect=["Test Gallery", "Test Description", "photo.jpg", "example.com"],
    )
    def test_new_google_gallery_created(self, input):
        with TempDirectory() as tempdir:
            sys.argv = [
                "gallery_init",
                "https://photos.app.goo.gl/test",
                "-p",
                tempdir.path,
            ]
            gallery_init.main()

            check_gallery_files(tempdir, [], [])
            self.check_gallery_config(
                os.path.join(tempdir.path, "gallery.json"),
                tempdir.path,
                "Test Gallery",
                "Test Description",
                160,
                "photo.jpg",
                "example.com",
                "google",
                "https://photos.app.goo.gl/test",
            )

    @mock.patch(
        "builtins.input",
        side_effect=["Test Gallery", "Test Description", "photo.jpg", "example.com"],
    )
    def test_new_invalid_remote_gallery(self, input):
        with TempDirectory() as tempdir:
            sys.argv = ["gallery_init", "https://test.com/test", "-p", tempdir.path]

            with self.assertRaises(SystemExit) as cm:
                gallery_init.main()
            self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
