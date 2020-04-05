# Usage

This section describes in detail how to use the Simple Photo Gallery command line tools.

## Create a new gallery (`gallery-init`)

The `gallery-init` command is used to create a new gallery.

### Folder with photos

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

### Online album

You can also create a gallery from an online album on [OneDrive]https://onedrive.live.com/) or [Google Photos](https://www.google.com/photos/about/) (please let me know if you want support for other cloud providers). You need to create an album and get link that can be shared with other people (click on the share button).

> Note: currently only photos and no videos are supported.

```
gallery-init <link_to_shared_album>
```

Using an online album will not download the photos, but just create links to them.

> *Warning*: This is an experimental feature, because OneDrive and Google Photos don't officially support links to individual photos, but only to albums that can be viewed on their sites. Therefore, your gallery may stop working at some point.

