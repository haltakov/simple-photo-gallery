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

    photos = {}

    def create_thumbnails(self, force=False):
        """
        This function doesn't do anything, because the thumbnails are links to OneDrive
        :param force: Forces generation of thumbnails if set to true
        """
        pass

    def is_scroll_bottom(self,driver):
        return driver.execute_script("return document.querySelector('c-wiz[id]').scrollHeight-document.querySelector('c-wiz[id]').scrollTop-document.querySelector('c-wiz[id]').getBoundingClientRect().height == 0;")

    # Function to scroll down the page using JavaScript
    def scroll_down(self,driver):
        driver.execute_script(f"document.querySelector('c-wiz[id]').scrollBy(0, document.querySelector('c-wiz[id]').getBoundingClientRect().height);")

    def store_photos(self,new_photos):

        for new_photo in new_photos:
            photo_url = new_photo.get_attribute("data-latest-bg")
            photo_base_url, photo_name = parse_photo_link(photo_url)
            self.photos[photo_url] = {
                "photo_base_url": photo_base_url,
                "photo_name": photo_name
            }

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
        #options.headless = True
        options.add_argument("--width=1920")
        options.add_argument("--height=1500")
        spg_common.log(f"Starting Firefox webdriver...")
        driver = webdriver.Firefox(options=options, executable_path=webdriver_path)

        # Load the album page
        spg_common.log(f'Loading album from {self.gallery_config["remote_link"]}...')
        driver.get(self.gallery_config["remote_link"])

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-latest-bg]')))

        # Scroll until reaching the total scroll height
        while not self.is_scroll_bottom(driver):

            # Capture new elements
            new_elements = driver.find_elements(By.XPATH, '//div[@data-latest-bg]')

            # Add new elements to the seen set
            self.store_photos(new_elements)

            # Output information
            print(f"Scrolled, New Elements: {len(new_elements)}, Total Elements: {len(self.photos)}")

            # Scroll down
            self.scroll_down(driver)

            # Wait for new elements to load
            #could use a proper element check here instead of arbitrary wait
            time.sleep(1)

        spg_common.log(f"Photos found: {len(self.photos)}")
        current_photo = 1
        for photo_url in self.photos:
            #photo_url = photo.get_attribute("data-latest-bg")
            #photo_base_url, photo_name = parse_photo_link(photo_url)

            photo_base_url = self.photos[photo_url]['photo_base_url']
            photo_name = self.photos[photo_url]["photo_name"]

            spg_common.log(
                f"{current_photo}/{len(self.photos)}\t\tProcessing photo {photo_name}: {photo_url}"
            )
            current_photo += 1

            if "http" not in photo_url:
                continue

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
