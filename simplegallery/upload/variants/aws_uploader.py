import subprocess
import simplegallery.common as spg_common
from simplegallery.upload.base_uploader import BaseUploader


class AWSUploader(BaseUploader):
    def check_location(self, location):
        """
        Checks if the location is empty or not
        :param location: S3 bucket where the gallery should be uploaded
        :return: True if the location is not empty, False otherwise
        """
        if not location:
            spg_common.log("Location cannot be empty when uploading to AWS")

        return bool(location)

    def upload_gallery(self, location, gallery_path):
        """
        Upload the gallery to the specified location
        :param location: S3 bucket where the gallery should be uploaded
        :param gallery_path: path to the root of the public files of the gallery
        """
        # Add s3 protocol if needed
        if not location.startswith("s3://"):
            location = "s3://" + location

        # Add trailing / if needed
        if not location.endswith("/"):
            location += "/"

        # Build and execute the AWS S3 sync command
        aws_command = [
            "aws",
            "s3",
            "sync",
            gallery_path,
            location,
            "--exclude",
            ".DS_Store",
        ]

        spg_common.log(f"Uploading to AWS S3 at {location}")
        process = subprocess.run(aws_command)

        if process.returncode != 0:
            raise spg_common.SPGException("Could not sync with AWS S3")

        # Compute HTTP URL and display success message
        url = location.replace("s3://", "http://") + "index.html"
        spg_common.log(
            f"Upload finished successfully! You can access your gallery at: {url}"
        )
