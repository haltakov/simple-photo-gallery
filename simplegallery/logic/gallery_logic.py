from simplegallery.logic.variants.files_gallery_logic import FilesGalleryLogic
from simplegallery.logic.variants.onedrive_gallery_logic import OnedriveGalleryLogic
from simplegallery.logic.variants.google_gallery_logic import GoogleGalleryLogic
import simplegallery.common as spg_common


def get_gallery_logic(gallery_config):
    """
    Factory function that returns an object of a class derived from BaseGalleryLogic based on the gallery config.
    Supported gallery logics:
    - FilesGalleryLogic - logic for local files gallery
    - OneDriveGallerLogic - logic for shared album from OneDrive
    - GoogleGallerLogic - logic for shared album from Google Photos

    :param gallery_config: gallery config dictionary as read from the gallery.json
    :return: gallery logic object
    """
    if "remote_gallery_type" not in gallery_config:
        return FilesGalleryLogic(gallery_config)
    elif not gallery_config["remote_gallery_type"]:
        return FilesGalleryLogic(gallery_config)
    elif gallery_config["remote_gallery_type"] == "onedrive":
        return OnedriveGalleryLogic(gallery_config)
    elif gallery_config["remote_gallery_type"] == "google":
        return GoogleGalleryLogic(gallery_config)
    else:
        spg_common.log(
            "Unrecognized option for remote_gallery_type. Proceeding as a local gallery."
        )
        return FilesGalleryLogic(gallery_config)


def get_gallery_type(remote_link):
    """
    Get the type of a remote gallery based on the provided link
    :param remote_link: Link to a shared album
    :return: remote gallery type
    """

    if "onedrive.live.com/" in remote_link or "1drv.ms/" in remote_link:
        return "onedrive"
    elif "photos.app.goo.gl/" in remote_link or "photos.google.com" in remote_link:
        return "google"
    elif "amazon.com/photos/" in remote_link:
        spg_common.log("Amazon is not currently supported as a remote gallery")
        return ""
    elif "share.icloud.com/" in remote_link:
        spg_common.log("iCloud is not currently supported as a remote gallery")
        return ""
    elif "www.dropbox.com/" in remote_link:
        spg_common.log("Dropbox is not currently supported as a remote gallery")
        return ""
    else:
        return ""
