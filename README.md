# Simple Photo Gallery

With Simple Photo Gallery you can easily create static HTML galleries that you can host yourself. Check out the [example gallery](http://www.haltakov.net/gallery_usa_multi/CUPcTB5AcbutK3vyLQ26/).

[![Example gallery](https://github.com/haltakov/simple-photo-gallery/raw/master/examples/screenshot_gallery_use_multi.png)](http://www.haltakov.net/gallery_usa_multi/CUPcTB5AcbutK3vyLQ26/)


## Overview

Simple Photo Gallery is a Python package that provides a simple command line interface to create static HTML photo and video galleries. Thumbnails, HTML, CSS and JavaScript files are generated automatically and you can just upload them to any static hosting, like for example [AWS S3](https://aws.amazon.com/s3/). The most important features:

* Responsive layout suitable for any device.
* Touch gestures support.
* Support for JPG, GIF and MP4 files.
* Image captions extracted from the image metadata (EXIF tags).
* Sensible defaults for very quick gallery setup.
* Easy customization of the gallery.
* Based on the [PhotoSwipe](https://photoswipe.com/) JavaScript library.


## Installation

Simple Photo Gallery is available as a Python package that you can install with `pip`. It installs several scripts to easily create galleries.
```
pip install simple-photo-gallery
```


## Usage

You can create a gallery is very simple and requires just 3 steps:

1. Collect all the photos and videos you want to have in the gallery into a folder.
2. On the terminal go to the folder with your photos and use the following command to initialize the gallery:
```
gallery_init
```
The script will ask you a few questions, like gallery name or background image. You can always just press Enter for the default settings and change them later.

3. To generate the photos' thumbnails and to create the gallery HTML, CSS and JS files use the following command:
```
gallery-build
```

