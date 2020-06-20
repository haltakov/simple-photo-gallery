import unittest
from unittest import mock
from unittest.mock import Mock
import os
import json
from testfixtures import TempDirectory
import simplegallery.upload.variants.netlify_uploader as netlify
from simplegallery.upload.uploader_factory import get_uploader


class NetlifyUploaderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.uploader = get_uploader("netlify")

    def test_netlify_without_location(self):
        self.assertTrue(self.uploader.check_location(""))

    @mock.patch("webbrowser.open")
    def test_get_authorization_token(self, webbrowser_open):
        # Create a mock HTTP server
        httpd = Mock()
        httpd.token = "test_token"

        # Check that the test token is returned
        self.assertEqual(httpd.token, self.uploader.get_authorization_token(httpd))

        # Patch the webbrowser call and check the URL
        webbrowser_open.assert_called_with(
            "https://app.netlify.com/authorize?response_type=token&"
            "client_id=f5668dd35a2fceaecbef1acd0b979a9d17484ae794df0c9b519b343ee2188596&"
            "redirect_uri=http://localhost:8080&"
            "state="
        )

    @mock.patch("requests.get")
    def test_get_netlify_site_id(self, requests_get):
        sites_mock = [
            dict(id="1", name="existing_site", url="http://www.existing_site.com"),
            dict(id="2", name="another__site", url="http://www.another_site.com"),
        ]
        response = Mock()
        response.text = json.dumps(sites_mock)
        requests_get.return_value = response

        self.assertEqual(
            "1", netlify.get_netlify_site_id("existing_site", "test_token")
        )
        self.assertEqual(None, netlify.get_netlify_site_id("", "test_token"))
        self.assertEqual(
            None, netlify.get_netlify_site_id("non_existing_site", "test_token")
        )

    @mock.patch("requests.post")
    @mock.patch("requests.put")
    def test_deploy_to_netlify(self, requests_put, requests_post):
        with TempDirectory() as tempdir:
            tempdir.write("test.zip", b"Test")
            zip_path = os.path.join(tempdir.path, "test.zip")

            # Mock the response to the deploy call
            response = Mock()
            response.text = '{"subdomain": "test"}'
            requests_post.return_value = response
            requests_put.return_value = response

            headers = {
                "Authorization": f"Bearer test_token",
                "Content-Type": "application/zip",
            }

            # Test with new site
            self.assertEqual(
                "https://test.netlify.com",
                netlify.deploy_to_netlify(zip_path, "test_token", None),
            )
            requests_post.assert_called_with(
                "https://api.netlify.com/api/v1/sites", headers=headers, data=b"Test"
            )

            # Test with existing site
            self.assertEqual(
                "https://test.netlify.com",
                netlify.deploy_to_netlify(zip_path, "test_token", "1"),
            )
            requests_put.assert_called_with(
                "https://api.netlify.com/api/v1/sites/1", headers=headers, data=b"Test"
            )

    @mock.patch("simplegallery.upload.variants.netlify_uploader.get_netlify_site_id")
    @mock.patch("simplegallery.upload.variants.netlify_uploader.deploy_to_netlify")
    @mock.patch(
        "simplegallery.upload.variants.netlify_uploader.NetlifyUploader.get_authorization_token"
    )
    def test_upload_gallery(
        self, get_authorization_token, deploy_to_netlify, get_netlify_site_id
    ):
        with TempDirectory() as tempdir:
            # Setup mock file
            tempdir.write("index.html", b"")
            # Set Natlify API call mocks
            get_netlify_site_id.return_value = "[]"
            get_authorization_token.return_value = "test_token"
            deploy_to_netlify.return_value = "test_url"

            self.uploader.upload_gallery("", tempdir.path)


if __name__ == "__main__":
    unittest.main()
