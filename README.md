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
2. Open a terminal go to the folder with your photos. Use the following command to initialize the gallery. The script will ask you a few questions, like gallery name or background image. You can always just press Enter for the default settings and change them later.
```
gallery_init
```

3. To generate the photos' thumbnails and to create the gallery HTML, CSS and JS files use the following command:
```
gallery-build
```

You are ready! You can view it by opening the `index.html` file in the `public` folder. The `public` folder contains all the files you need for your gallery and you can host it on any static hosting provider.

> **Note**
> Your photos and videos are copied in `public/images/photos`.

See below for more details how you can customize your gallery.


### Gallery configuration (`gallery.json`)

The `gallery.json` file in the gallery root folder contains important settings for the gallery. Some of them are filled by the questions asked by the `gallery-init` command, while others are settings used by other scripts. You can modify the following configurations to customize your gallery. You can also take a look at `gallery.json` of the [example gallery](https://github.com/haltakov/simple-photo-gallery/blob/create_readme/examples/gallery_usa_multi/gallery.json).

* `title` - the title of the gallery shown in the browser title and on the overview image. Example: `"USA Trip 2019"`.
* `description` - a longer text shown under the title on the overview image. Example: `"We took a road trip with an RV..."`.
* `background_photo` - the file name of the photo that should be used as background image. Example: `"usa-170.jpg"`.
* `background_photo_offset` - the vertical offset of the overview image in percentage. Use this to shift the portion of the overview image that is shown to focus on the most important pars. Example: `30`.
