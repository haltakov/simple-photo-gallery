from simplegallery.logic.files_gallery_logic import FilesGalleryLogic


def get_gallery_logic(gallery_config):
    """
    Factory function that returns an object of a class derived from BaseGalleryLogic based on the gallery config.
    Supported gallery logics:
    - FilesGalleryLogic - logic for local files gallery

    :param gallery_config: gallery config dictionary as read from the gallery.json
    :return: gallery logic object
    """
    return FilesGalleryLogic(gallery_config)


def get_gallery_type(remote_link):
    """
    Get the type of a remote gallery based on the provided link
    :param remote_link: Link to a shared album
    :return: remote gallery type
    """

    return ""
