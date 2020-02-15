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

Simple Photo Gallery is available as a Python package, which installs several scripts to easily create galleries. You can install it using `pip`:

```
pip install simple-photo-gallery
```

## Usage