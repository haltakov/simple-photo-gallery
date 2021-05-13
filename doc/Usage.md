# Usage

This section describes in detail how to use the Simple Photo Gallery command line tools.

* [Start a new gallery (`gallery-init`)](#start-a-new-gallery-gallery-init)
  * [Folder with photos/videos](#folder-with-photosvideos)
  * [Online album](#online-album)
* [Build the gallery files (`gallery-build`)](#build-the-gallery-files-gallery-build)
* [Publishing your gallery (`gallery-upload`)](#publishing-your-gallery-gallery-upload)
  * [Uploading to Netlify](#uploading-to-netlify)
  * [Uploading to AWS S3](#uploading-the-aws-s3)

## Start a new gallery (`gallery-init`)

The `gallery-init` command is used to create a new gallery.

### Folder with photos/videos

If you want to create a new gallery from a folder containing your photos you can just call it from the folder and it will create all the required files.

> **Note**
> Your photos and videos are copied in `public/images/photos`.

```
gallery-init
```

Alternatively, you can also provide a path to a folder where the photos are stored.

```
gallery-init -p <path/to/photos>
```

The script will ask you to provide some input in order to customize your gallery, like title, description, background photo or URL. You can always just press Enter to skip the question and then modify the `gallery.json` file manually. See [Basic Configuration](GalleryConfiguration.md#basic-configuration-galleryjson) for more details.

### Online album

> *Warning*: This is an experimental feature, because OneDrive and Google Photos don't officially support links to individual photos, but only to albums that can be viewed on their web sites. Therefore, your gallery may stop working at some point in time.

> Note: currently only photos and no videos are supported.

You can also create a gallery from an online album on [OneDrive](https://onedrive.live.com/) or [Google Photos](https://www.google.com/photos/about/) (please let me know if you want support for other cloud providers). You need to create an album and get link that can be shared with other people (click on the share button).

```
gallery-init <link_to_shared_album>
```

Using an online album will not download the photos, but just create links to them.

### Skip questions on the console

You can skip asking questions on the console by the script with the following parameter. In this case the defaults will be used to create the configuration.

```
gallery-init --use-defaults
```


## Build the gallery files (`gallery-build`)

The `gallery-build` command is used to create all files needed to display the gallery in the `public` folder: thumbnails of images, HTML files and CSS and JavaScript files.

You can directly call the `gallery-build` command from a folder that contains a gallery (`gallery.json` file):

```
gallery-build
```

Alternatively, you can also pass the path to a folder, where the gallery is located:

```
gallery-build -p <path/to/gallery>
```

The option `-ft` or `--force-thumbnails` can be used to trigger the generation of the thumbnails again.

```
gallery-build -ft
```

In order for your HTML gallery to be updated, You should call the `gallery-build` command every time that you make changes to the gallery (`gallery.json`), the image descriptions (`images_data.json`), HTML templates (`templates/index_template.jinja`) or the photos and videos.


## Publishing your gallery (`gallery-upload`)

After your gallery is built, you can either upload it manually to your hosting provider or you can use one of the automatic upload options.

### Uploading to Netlify

[Netlify](https://www.netlify.com/) offers a [free hosting plan](https://www.netlify.com/pricing/) for static websites. First, you need to [create a free account](https://app.netlify.com/signup) on Netlify and then you can just call the `gallery-upload` command from the folder containing your gallery to create a new site:

```
gallery-upload netlify
```

You will then need to give permissions to the Simple Photo Gallery app on Netlify to create websites for you. After that the gallery will be uploaded, a new website will be created and it will be opened in your browser. You can then log in to your Netlify account and change the website's name or link it to a [custom domain](https://docs.netlify.com/domains-https/custom-domains/).

If you want to upload to an existing site, you can specify its name or URL in the `gallery.json` file as `remote_location` or provide it as a parameter:

```
gallery-upload netlify <site_name>
```

> Note: it is not recommended uploading huge galleries to Netlify, because you may exceed the quota of the free account. In this case, it is better to upload the photos to OneDrive or Google Photos and create the gallery from the online album. In this way, you will just need to upload the HTML, JavaScript and CSS files to Netlify, which are very small.


### Uploading the AWS S3

To use the automatic upload to [AWS S3](https://aws.amazon.com/s3/) you need to have a AWS account and to create a bucket in S3 that is publicly visible (see the [AWS tutorial](https://aws.amazon.com/getting-started/projects/host-static-website/). You also need to setup the [Amazon Command Line Interface](https://aws.amazon.com/cli/) in your environment, because the `gallery-upload` command will call `aws s3 sync` command.

Once your setup is done, you can call `gallery-upload`:

```
gallery-upload aws s3://<bucket>/<path>
```

Alternatively, you can also put your bucket and path in the `gallery.json` file under `remote_location`.











