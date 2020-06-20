import time
import pkg_resources
import simplegallery.common as spg_common
import simplegallery.media as spg_media
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from simplegallery.logic.base_gallery_logic import BaseGalleryLogic


def parse_photo_link(photo_url):
    """
    Extracts the base URL (URL without query parameters) and the photo name from a Onedrive photo URL
    :param photo_url: photo URL
    :return: base URL and photo name
    """
    base_url = photo_url.split("=")[0]
    name = base_url.split("/")[-1]

    return base_url, name


class GoogleGalleryLogic(BaseGalleryLogic):
    def create_thumbnails(self, force=False):
        """
        This function doesn't do anything, because the thumbnails are links to OneDrive
        :param force: Forces generation of thumbnails if set to true
        """
        pass

    def generate_images_data(self, images_data):
        """
        Parse the remote link and extract link to the images and the thumbnails
        :param images_data: Images data dictionary containing the existing metadata of the images and which will be
        updated by this function
        :return updated images data dictionary
        """

        # Get the path to the Firefox webdriver
        webdriver_path = pkg_resources.resource_filename(
            "simplegallery", "bin/geckodriver"
        )

        # Configure the driver in headless mode
        options = Options()
        options.headless = True
        spg_common.log(f"Starting Firefox webdriver...")
        driver = webdriver.Firefox(options=options, executable_path=webdriver_path)

        # Load the album page
        spg_common.log(f'Loading album from {self.gallery_config["remote_link"]}...')
        driver.get(self.gallery_config["remote_link"])

        # Wait until the page is fully loaded
        loading_start = time.time()
        last_image_count = 0
        while True:
            image_count = len(driver.find_elements_by_xpath("//div[@data-latest-bg]"))
            if image_count > 1 and image_count == last_image_count:
                break
            last_image_count = image_count
            if (time.time() - loading_start) > 30:
                raise spg_common.SPGException("Loading the page took too long.")
            time.sleep(5)

        # Parse all photos
        spg_common.log("Finding photos...")
        photos = driver.find_elements_by_xpath("//div[@data-latest-bg]")

        spg_common.log(f"Photos found: {len(photos)}")
        current_photo = 1
        for photo in photos:
            photo_url = photo.get_attribute("data-latest-bg")
            photo_base_url, photo_name = parse_photo_link(photo_url)
            spg_common.log(
                f"{current_photo}/{len(photos)}\t\tProcessing photo {photo_name}: {photo_url}"
            )
            current_photo += 1

            # Compute photo and thumbnail sizes
            photo_link_max_size = f"{photo_base_url}=w9999-h9999-no"
            size = spg_media.get_remote_image_size(photo_link_max_size)
            thumbnail_size = spg_media.get_thumbnail_size(
                size, self.gallery_config["thumbnail_height"]
            )

            # Add the photo to the images_data dict
            images_data[photo_name] = dict(
                description="",
                mtime=time.time(),
                size=size,
                src=f"{photo_base_url}=w{size[0]}-h{size[1]}-no",
                thumbnail=f"{photo_base_url}=w{thumbnail_size[0]}-h{thumbnail_size[1]}-no",
                thumbnail_size=thumbnail_size,
                type="image",
            )

        spg_common.log(f"All photos processed!")

        driver.quit()

        return images_data
