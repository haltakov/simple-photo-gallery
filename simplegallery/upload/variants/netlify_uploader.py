import os
import json
import webbrowser
import requests
import zipfile
import jinja2
import pkg_resources
import tempfile
import time
from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import simplegallery.common as spg_common
from simplegallery.upload.base_uploader import BaseUploader


class SimplePhotoGalleryHTTPServer(HTTPServer):
    token = ''
    error_detected = False


class SimplePhotoGalleryHTTPRequestHandler(BaseHTTPRequestHandler):

    def get_params(self):
        return dict(parse.parse_qsl(parse.urlsplit(self.path).query))

    def render_page(self, page, data, status):
        self.send_response(status)
        self.end_headers()

        file_loader = jinja2.FileSystemLoader(pkg_resources.resource_filename('simplegallery', 'data/netlify'))
        env = jinja2.Environment(loader=file_loader)
        template = env.get_template(page)
        self.wfile.write(template.render(data=data).encode('utf-8'))

    def process_index(self):
        self.render_page('index.jinja', [], 200)

    def process_token(self):
        params = self.get_params()

        if 'access_token' in params:
            self.server.token = params['access_token']
            self.render_page('deploy.jinja', [], 200)
        else:
            self.process_error('Did not receive a valid access token')

    def process_error(self, message):
        self.server.error_detected = True
        self.render_page('error.jinja', dict(message=message), 400)

    # Suppress the logging
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path == '/':
            self.process_index()
        elif self.path.startswith('/token'):
            self.process_token()
        else:
            self.process_error('Invalid request')


class NetlifyUploader(BaseUploader):
    client_id = 'f5668dd35a2fceaecbef1acd0b979a9d17484ae794df0c9b519b343ee2188596'
    client_secret = '9283bc00893b493c8b4e1ceed167dd4463767362b6ae669ccb5f513f2704d876'
    redirect_uri = 'http://localhost:8080'
    state = ''

    def check_location(self, location):
        return True

    def create_website_zip(self, gallery_path, zip_file_path):
        zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

        for root, dirs, files in os.walk(gallery_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=os.path.relpath(file_path, gallery_path))

        zip_file.close()

    def get_authorization_token(self, httpd):
        # Open the Netlify authorization page
        auth_code_url = f'https://app.netlify.com/authorize?' + \
                        f'response_type=token&' + \
                        f'client_id={self.client_id}&' + \
                        f'redirect_uri={self.redirect_uri}&' + \
                        f'state={self.state}'
        webbrowser.open(auth_code_url)

        # Process requests until the server receives the token
        while not httpd.token and not httpd.error_detected:
            httpd.handle_request()

        return httpd.token

    def deploy_to_netlify(self, zip_file_path, token):
        # Read the content of the ZIP file
        with open(zip_file_path, 'rb') as zip_in:
            gallery_data = zip_in.read()

        sites_url = 'https://api.netlify.com/api/v1/sites'
        headers = {'Authorization': f'Bearer {token}',
                   'Content-Type': 'application/zip'}

        spg_common.log('Uploading gallery to Netlify...')
        r = requests.post(sites_url, headers=headers, data=gallery_data)
        response = json.loads(r.text)

        return response.get('url')

    def upload_gallery(self, location, gallery_path):
        # Create a zip file for the gallery
        spg_common.log('Creating ZIP file of the gallery...')
        zip_file_path = os.path.join(tempfile.gettempdir(), 'simple_photo_gallery.zip')
        self.create_website_zip(gallery_path, zip_file_path)
        spg_common.log('Gallery ZIP file created!')

        # Start the HTTP server that handles OAuth authentication at Netlify
        httpd = SimplePhotoGalleryHTTPServer(('localhost', 8080), SimplePhotoGalleryHTTPRequestHandler)

        # Get the authorization token
        token = self.get_authorization_token(httpd)

        # Deploy the website
        gallery_url = self.deploy_to_netlify(zip_file_path, token)

        # Delete the zip file
        os.remove(zip_file_path)

        # Open the Netlify gallery if successful
        if gallery_url:
            spg_common.log(f'Gallery uploaded successfully to:\n{gallery_url}')
            webbrowser.open(gallery_url)
        else:
            raise spg_common.SPGException(f'Something went wrong while uploading to Netlify')


