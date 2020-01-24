import argparse
import logging
import simplegallery.common as spg_common


def parse_args():
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    description = '''Builds the HTML gallery, generating all required files for display.'''

    parser = argparse.ArgumentParser(description=description)

    return parser.parse_args()


def main():
    # Init the logger
    spg_common.setup_gallery_logging()


if __name__ == "__main__":
    main()

