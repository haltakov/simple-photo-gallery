import unittest
from unittest import mock
from unittest.mock import Mock
import os
import subprocess
from testfixtures import TempDirectory
import simplegallery.upload.variants.netlify_uploader as netlify
from simplegallery.upload.uploader_factory import get_uploader


class NetlifyUploaderTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.uploader = get_uploader('netlify')

    def test_netlify_without_location(self):
        self.assertTrue(self.uploader.check_location(''))

    @mock.patch('webbrowser.open')
    def test_get_authorization_token(self, webbrowser_open):
        # Create a mock HTTP server
        httpd = Mock()
        httpd.token = 'test_token'

        # Check that the test token is returned
        self.assertEqual(httpd.token, self.uploader.get_authorization_token(httpd))

        # Patch the webbrowser call and check the URL
        webbrowser_open.assert_called_with(
            'https://app.netlify.com/authorize?response_type=token&'
            'client_id=f5668dd35a2fceaecbef1acd0b979a9d17484ae794df0c9b519b343ee2188596&'
            'redirect_uri=http://localhost:8080&'
            'state='
        )

    @mock.patch('requests.post')
    def test_deploy_to_netlify(self, requests_post):
        with TempDirectory() as tempdir:
            tempdir.write('test.zip', b'Test')

            # Mock the response to the deploy call
            response = Mock()
            response.text = '{"url": "test_url"}'
            requests_post.return_value = response

            self.assertEqual('test_url', netlify.deploy_to_netlify(os.path.join(tempdir.path, 'test.zip'), 'test_token'))

            # Check that the deploy call was correct
            headers = {'Authorization': f'Bearer test_token',
                       'Content-Type': 'application/zip'}
            requests_post.assert_called_with('https://api.netlify.com/api/v1/sites',
                                             headers=headers,
                                             data=b'Test')

    @mock.patch('simplegallery.upload.variants.netlify_uploader.deploy_to_netlify')
    @mock.patch('simplegallery.upload.variants.netlify_uploader.NetlifyUploader.get_authorization_token')
    def test_upload_gallery(self, get_authorization_token, deploy_to_netlify):
        with TempDirectory() as tempdir:
            # Setup mock file
            tempdir.write('index.html', b'')
            # Set Natlify API call mocks
            get_authorization_token.return_value = 'test_token'
            deploy_to_netlify.return_value = 'test_url'

            self.uploader.upload_gallery('', tempdir.path)


if __name__ == '__main__':
    unittest.main()
