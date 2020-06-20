class BaseUploader:
    """
    Base class defining the interface to a remote uploader.
    """

    def check_location(self, location):
        """
        Checks if the provided location for the upload is valid or not
        :param location: location where the gallery will be uploaded (uploader specific)
        :return: True if the location is valid, False otherwise
        """
        pass

    def upload_gallery(self, location, gallery_path):
        """
        Upload the gallery to the specified location
        :param location: location where the gallery will be uploaded (uploader specific)
        :param gallery_path: path to the root of the public files of the gallery
        """
        pass
