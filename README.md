# Simple Photo Gallery

### Check out the new [Project Page](https://haltakov.net/simple-photo-gallery)!

With Simple Photo Gallery you can create beautiful and simple photo galleries that help you tell your story. Check out the [example gallery](https://www.haltakov.net/simple-photo-gallery/gallery_usa_multi/).

[![Example gallery](https://github.com/haltakov/simple-photo-gallery/blob/master/examples/gallery_usa_multi/screenshot_gallery_usa_multi.jpg?raw=true)](https://www.haltakov.net/simple-photo-gallery/gallery_usa_multi/)


## Overview

1. [Installation](#installation)
2. [Usage](#usage)
3. [Hosting](#hosting)
4. [Configuration](#configuration)
5. [About](#about)

Simple Photo Gallery is a simple command line tool written in Python that helps you create static HTML photo and video galleries that tell a story. Thumbnails, HTML, CSS and JavaScript files are generated automatically and can be uploaded to any static hosting, like for example [AWS S3](https://aws.amazon.com/s3/) or [Netlify](https://www.netlify.com/). The most important features:

* Responsive layout suitable for any device (including touch gestures support).
* Image captions extracted from the image metadata (EXIF tags).
* Fully customizable layout with sensible defaults to get started quickly.
* Create a gallery from an existing OneDrive or Google Photos album, without downloading the photos.
* Automatic upload of the gallery to [AWS S3](https://aws.amazon.com/s3/) or [Netlify](https://www.netlify.com/).
* Based on the [PhotoSwipe](https://photoswipe.com/) JavaScript library.

## Installation

Simple Photo Gallery can be easily installed with `pip`. If you don't have `pip`, please install the [latest Python release](https://www.python.org/downloads/).
```
pip install simple-photo-gallery
```

## Example Usage

You can quickly create a gallery with the default settings. For more detailed information see [Usage](doc/Usage.md).

1. Collect all the photos and videos you want to have in the gallery into a folder.
2. Open a terminal and go to the folder with your photos. Use the following command to initialize the gallery. The script will ask you a few questions, like gallery name or background image. You can always just press Enter for the default settings and change them later.
```
gallery-init
```

3. To generate the photos' thumbnails and to create the gallery HTML, CSS and JS files use the following command:
```
gallery-build
```

The gallery is ready! You can view it by opening the `index.html` file in the `public` folder. The `public` folder contains all the files you need for your gallery and you can host it on any static hosting provider.

> **Note**
> Your photos and videos are copied in `public/images/photos`.

4. Optionally, you can directly publish the gallery on [Netlify](https://www.netlify.com/), which offers a free plan.

See [Gallery Configuration](doc/GalleryConfiguration.md) for more details how you can customize your gallery. You can also find two example galleries in the [`examples`](https://github.com/haltakov/simple-photo-gallery/tree/master/examples) folder.


## Hosting

You can automatically upload the gallery to [AWS S3](https://aws.amazon.com/s3/) or [Netlify](https://www.netlify.com/).

For Netlify you just need a free account and then you can run the following command to upload to a new website.
```
gallery-upload netlify
```

For AWS S3 you need to have [Amazon Command Line Interface](https://aws.amazon.com/cli/) installed and configured and a bucket that can be accessed publicly (see the [AWS tutorial](https://aws.amazon.com/getting-started/projects/host-static-website/) for hosting a static website).
```
gallery-upload aws s3://<your_bucket>/<path>/
```

You can upload your gallery manually on any static hosting provider, like for example [AWS S3](https://aws.amazon.com/s3/), [GitHub Pages](https://pages.github.com/), [Netlify](https://www.netlify.com/) or others. Some scripts for automatic upload of the gallery are under work.


## About

Simple Photo Gallery is developed by [Vladimir Haltakov](https://www.haltakov.net). I wanted an easy way to share photos with friends, but wasn't happy with the limited customization options that existing sharing solutions like Amazon Photos or iCloud offer.

Please contact me on [Twitter](https://twitter.com/haltakov) if you have any questions, ideas for improvement or feature requests.