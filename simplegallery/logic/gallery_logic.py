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