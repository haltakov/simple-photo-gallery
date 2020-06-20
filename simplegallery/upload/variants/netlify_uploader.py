import os
import json
import webbrowser
import requests
import zipfile
import jinja2
import pkg_resources
import tempfile
from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import simplegallery.common as spg_common
from simplegallery.upload.base_uploader import BaseUploader


class SimplePhotoGalleryHTTPServer(HTTPServer):
    """
    Class deriving from the HTTPServer, defining new properties
    """

    """
    Authentication token that was sent to the server by the Netlify API
    """
    token = ""

    """
    Flag specifying if an error occurred during the OAuth 2.0 process
    """
    error_detected = False


class SimplePhotoGalleryHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Class implementing the handling of the OAUth 2.0 process with the Netlify API
    """

    def get_params(self):
        """
        Get the parameters of the URL the request handler is processing
        :return: dict with URL parameters
        """
        return dict(parse.parse_qsl(parse.urlsplit(self.path).query))

    def render_page(self, page, data, status):
        """
        Renders a Jinja2 template and writes it in the handler's repsonse
        :param page: name of the page to be rendered
        :param data: data to be passed to the Jinja2 template
        :param status: response status code
        """
        self.send_response(status)
        self.end_headers()

        file_loader = jinja2.FileSystemLoader(
            pkg_resources.resource_filename("simplegallery", "data/netlify")
        )
        env = jinja2.Environment(loader=file_loader)
        template = env.get_template(page)
        self.wfile.write(template.render(data=data).encode("utf-8"))

    def process_index(self):
        """
        Renders the default index page
        """
        self.render_page("index.jinja", [], 200)

    def process_token(self):
        """
        Retrieves the authentication token from the URL's parameters or raises an error
        """
        params = self.get_params()

        if "access_token" in params:
            self.server.token = params["access_token"]
            self.render_page("deploy.jinja", [], 200)
        else:
            self.process_error("Did not receive a valid access token")

    def process_error(self, message):
        """
        Renders an error page
        :param message: error message
        """
        self.server.error_detected = True
        self.render_page("error.jinja", dict(message=message), 400)

    def log_message(self, format, *args):
        """
        Suppresses the logging of the HTTP server
        """
        return

    def do_GET(self):
        """
        Handles GET requests to the server
        """
        if self.path == "/":
            self.process_index()
        elif self.path.startswith("/token"):
            self.process_token()
        else:
            self.process_error("Invalid request")


def get_netlify_site_id(location, token):
    """
    Retrieves the ID of a site from the Netlify API
    :param location: name of the Netlify site
    :param token: OAuth 2.0 authentication token
    :return: the site ID if the site exists, None otherwise
    """

    # Check if location invalid
    if location:
        sites_url = "https://api.netlify.com/api/v1/sites"
        headers = {"Authorization": f"Bearer {token}"}

        response_string = requests.get(sites_url, headers=headers)
        sites = json.loads(response_string.text)

        for site in sites:
            if site["name"] == location or site["url"].endswith(location):
                spg_common.log(f"Found Netlify site: {location}")
                return site["id"]
    else:
        spg_common.log(f"Cannot find Netlify site {location}. Creating new site...")
        return None


def deploy_to_netlify(zip_file_path, token, site_id):
    """
    Deploys the gallery to Netlify using the Deploy API
    :param zip_file_path: path to the zip file containing the gallery's files
    :param token: OAuth 2.0 authentication token
    :param site_id: ID of the Netlify site (optional - if no ID is provided, a new site will be created)
    :return: URL to the site where the gallery was uploaded
    """
    # Read the content of the ZIP file
    with open(zip_file_path, "rb") as zip_in:
        gallery_data = zip_in.read()

    sites_url = "https://api.netlify.com/api/v1/sites" + (
        f"/{site_id}" if site_id else ""
    )
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/zip"}

    spg_common.log("Uploading gallery to Netlify...")

    if site_id:
        response_string = requests.put(sites_url, headers=headers, data=gallery_data)
    else:
        response_string = requests.post(sites_url, headers=headers, data=gallery_data)

    response = json.loads(response_string.text)

    return f'https://{response.get("subdomain")}.netlify.com'


def create_website_zip(gallery_path, zip_file_path):
    """
    Create a ZIP archive of the gallery's public files
    :param gallery_path: path to the public files of the gallery
    :param zip_file_path: path where the zip file should be stored
    """
    zip_file = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(gallery_path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_file.write(file_path, arcname=os.path.relpath(file_path, gallery_path))

    zip_file.close()


class NetlifyUploader(BaseUploader):
    client_id = "f5668dd35a2fceaecbef1acd0b979a9d17484ae794df0c9b519b343ee2188596"
    client_secret = "9283bc00893b493c8b4e1ceed167dd4463767362b6ae669ccb5f513f2704d876"
    redirect_uri = "http://localhost:8080"
    state = ""

    def check_location(self, location):
        """
        Always returns True, because the uploader will create a new site if no location is provided or is invalid
        (authentication is required to check if the site exists)
        :param location: Netlify site where the gallery should be uploaded
        :return: True
        """
        return True

    def get_authorization_token(self, httpd):
        """
        Retrieve an OAuth 2.0 authentication token from the Netlify API
        :param httpd: HTTP Server performing the OAuth 2.0 authentication
        :return: authentication token
        """
        # Open the Netlify authorization page
        auth_code_url = (
            f"https://app.netlify.com/authorize?"
            + f"response_type=token&"
            + f"client_id={self.client_id}&"
            + f"redirect_uri={self.redirect_uri}&"
            + f"state={self.state}"
        )
        webbrowser.open(auth_code_url)

        # Process requests until the server receives the token
        while not httpd.token and not httpd.error_detected:
            httpd.handle_request()

        return httpd.token

    def upload_gallery(self, location, gallery_path):
        """
        Upload the gallery to the specified location
        :param location: Netlify site where the gallery should be uploaded
        :param gallery_path: path to the root of the public files of the gallery
        """
        # Create a zip file for the gallery
        spg_common.log("Creating ZIP file of the gallery...")
        zip_file_path = os.path.join(tempfile.gettempdir(), "simple_photo_gallery.zip")
        create_website_zip(gallery_path, zip_file_path)
        spg_common.log("Gallery ZIP file created!")

        # Start the HTTP server that handles OAuth authentication at Netlify
        httpd = SimplePhotoGalleryHTTPServer(
            ("localhost", 8080), SimplePhotoGalleryHTTPRequestHandler
        )

        # Get the authorization token
        token = self.get_authorization_token(httpd)

        # Check if the website already exists and get its ID
        site_id = get_netlify_site_id(location, token)

        # Deploy the website
        gallery_url = deploy_to_netlify(zip_file_path, token, site_id)

        # Delete the zip file
        os.remove(zip_file_path)

        # Open the Netlify gallery if successful
        if gallery_url:
            spg_common.log(f"Gallery uploaded successfully to:\n{gallery_url}")
            webbrowser.open(gallery_url)
        else:
            raise spg_common.SPGException(
                f"Something went wrong while uploading to Netlify"
            )
