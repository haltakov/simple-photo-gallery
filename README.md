# Simple Photo Gallery

With Simple Photo Gallery you can easily create static HTML galleries that you can host yourself. Check out the [example gallery](http://www.haltakov.net/gallery_usa_multi/CUPcTB5AcbutK3vyLQ26/index.html).

[![Example gallery](https://github.com/haltakov/simple-photo-gallery/blob/master/examples/gallery_usa_multi/screenshot_gallery_usa_multi.jpg?raw=true)](http://www.haltakov.net/gallery_usa_multi/CUPcTB5AcbutK3vyLQ26/index.html)


## Overview

1. [Installation](#installation)
2. [Usage](#usage)
3. [Hosting](#hosting)
4. [Configuration](#configuration)
5. [About](#about)

Simple Photo Gallery is a Python package that provides a simple command line interface to create static HTML photo and video galleries. Thumbnails, HTML, CSS and JavaScript files are generated automatically and you can just upload them to any static hosting, like for example [AWS S3](https://aws.amazon.com/s3/). The most important features:

* Responsive layout suitable for any device (including touch gestures support).
* Image captions extracted from the image metadata (EXIF tags).
* Fully customizable layout with sensible defaults to get started quickly.
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
gallery-init
```

3. To generate the photos' thumbnails and to create the gallery HTML, CSS and JS files use the following command:
```
gallery-build
```

You are ready! You can view it by opening the `index.html` file in the `public` folder. The `public` folder contains all the files you need for your gallery and you can host it on any static hosting provider.

> **Note**
> Your photos and videos are copied in `public/images/photos`.

See the [Configuration](#configuration) section for more details how you can customize your gallery. You can also find two example galleries in the [`examples`](https://github.com/haltakov/simple-photo-gallery/tree/create_readme/examples) folder.


## Hosting

You can host your gallery on any static hosting provider, like for example [AWS S3](https://aws.amazon.com/s3/), [GitHub Pages](https://pages.github.com/), [Netlify](https://www.netlify.com/) or others. Some scripts for automatic upload of the gallery are under work.


## Configuration

The gallery is fully customizable. For the most common use-cases, there are some simple configuration options, described in details below.

### Gallery Configuration (`gallery.json`)

The `gallery.json` file in the gallery root folder contains important settings for the gallery. Some of them are filled by the questions asked by the `gallery-init` command, while others are settings used by other scripts. You can modify the following configurations to customize your gallery. You can also take a look at `gallery.json` of the [example gallery](https://github.com/haltakov/simple-photo-gallery/blob/create_readme/examples/gallery_usa_multi/gallery.json).

* `title` - the title of the gallery shown in the browser title and on the overview image. Example: `"USA Trip 2019"`.
* `description` - a longer text shown under the title on the overview image. Example: `"We took a road trip with an RV..."`.
* `background_photo` - the file name of the photo that should be used as background image. Example: `"usa-170.jpg"`.
* `background_photo_offset` - the vertical offset of the overview image in percentage. Use this to shift the portion of the overview image that is shown to focus on the most important pars. Example: `30`.


### Photo Captions

You can show a caption for each photo that is shown on the bottom of the image when looking at the gallery. There are two ways to specify the captions:

1. **Image metadata**: some photo editors, like for example Adobe Lightroom, allow you to define a description for each image. It is written in the image metadata and the `gallery-build` can read it from there. It reads the `ImageDescription` EXIF tag. All captions are then stored in the `images_data.json` file.
2. **Manually**: executing the `gallery-build` command will create a file called `images_data.json`. It contains some metadata for each photo and a property called `description` where you can enter the caption for each image.


### Sections

Using the default configuration, all photos will be displayed in one section, like in the [simple example gallery](https://github.com/haltakov/simple-photo-gallery/tree/create_readme/examples/gallery_usa_simple). If you want to display more photos, though, you may want to group your photos in sections and provide some additional title and description for each section, like in the [multi-section example gallery](https://github.com/haltakov/simple-photo-gallery/tree/create_readme/examples/gallery_usa_multi).

You can change the gallery layout in the `templates/index_template.jinja` file. This is basically a HTML file including some [Jinja](https://www.palletsprojects.com/p/jinja/) templates code. You can use the predefined macro to easily define sections. In the template, you will find the following code generated by default:

```
  {{ gallery_macros.section(0, images|length,
                               gallery_config['title'],
                               '',
                               images)}}
```
You can call the macro as many times as sections you want to have and modify its 5 parameters to specify each section:

* index of the first image in the section (0 by default)
* index of the first image in the next section (length of the `images` array by default)
* section title (by default this is the title from the configuration file)
* description text of the section (by default it is empty)
* the array containing the images data: `images` (don't change this)

In the [multi-section example gallery](https://github.com/haltakov/simple-photo-gallery/blob/create_readme/examples/gallery_usa_multi/templates/index_template.jinja), there are 3 sections defined like this:
```
{{ gallery_macros.section(0, 20,
                             'Joshua Tree National Park',
                             'We spent 2 days in Joshua Tree National park. We spent the first night in the Black Rock campground. After that we travelled through the park for the whole day visiting several interesting view points and trails. After we spent the second night in the Jumbo Rocks campground we left the park from the south exit stopping at several places along the way.',
                             images)}}
                             
{{ gallery_macros.section(20, 36,
                              'Sequoia and Kings Canyon National Park',
                              'We visited Sequoia and Kings Canyon National Park for another two nights. Since all campgrounds were still closed because of the cold weather we stayed at the John Muir and at the Wuksachi Lodge. We looked at the Giant Sequoias along several trails and also drove down the King\'s Canyon to do a tour of the amazing Zumwalt Meadows.',
                              images)}}
                              
{{ gallery_macros.section(36, images|length,
                              'San Francisco',
                              'Our trip ended in San Francisco, where we spent a lot of time in the great Golden Gate park and other must see places like the Embarcadero, Downtown and Alcatraz.',
                              images)}}
```

### Advanced Layout Configuration

Feel free to modify any part of the layout you want by just modifying the corresponding HTML, CSS or JavaScript files.


## About

Simple Photo Gallery is developed by [Vladimir Haltakov](http://www.haltakov.net). I wanted an easy way to share photos with friends, but wasn't happy with the limited customization options that existing sharing solutions like Amazon Photos or iCloud offer.

Please contact me if you have any questions, ideas for improvement or feature requests.