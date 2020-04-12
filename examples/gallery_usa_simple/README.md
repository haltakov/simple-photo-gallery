# Gallery USA Simple

This is an example gallery containing only one photo section. The gallery code without the photos is available on GitHub. You can view the gallery here: [https://www.haltakov.net/simple-photo-gallery/gallery_usa_simple/](https://www.haltakov.net/simple-photo-gallery/gallery_usa_simple/)

[![Example gallery simple](https://github.com/haltakov/simple-photo-gallery/blob/master/examples/gallery_usa_simple/screenshot_gallery_usa_simple.jpg?raw=true)](https://www.haltakov.net/simple-photo-gallery/gallery_usa_simple/)

## How to create this gallery

This gallery was created in the following way.

1. Initialize the gallery - execute the following command in the folder containing the images
```
gallery-init
```

2. Answer the questions asked by the script as shown below:
```
What is the title of your gallery? (default: "My Gallery")
> San Francisco 2019
What is the description of your gallery? (default: "Default description of my gallery")
> We visited San Francisco for a couple of days in May 2019 as part of our California trip.
Which image should be used as background for the header? (default: "")
> usa-494.jpg
```

3. Modify the `gallery.json` file to adjust the offset of the background image from 30% to 50%:

```
"background_photo_offset": 50
```

4. Build the gallery - execute the following command:
```
gallery-build
```

