# Gallery USA Simple

This is an example of a more complex gallery containing 3 photo sections. The gallery code without the photos is available on GitHub. You can view the gallery here: [https://www.haltakov.net/simple-photo-gallery/gallery_usa_multi/](https://www.haltakov.net/simple-photo-gallery/gallery_usa_multi/)

[![Example gallery simple](https://github.com/haltakov/simple-photo-gallery/blob/master/examples/gallery_usa_multi/screenshot_gallery_usa_multi.jpg?raw=true)](https://www.haltakov.net/simple-photo-gallery/gallery_usa_multi/)

## How to create this gallery

This gallery was created in the following way.

1. Initialize the gallery - execute the following command in the folder containing the images
```
gallery-init
```

2. Answer the questions asked by the script as shown below:
```
What is the title of your gallery? (default: "My Gallery")
> USA Trip 2019
What is the description of your gallery? (default: "Default description of my gallery")
> We took a road trip with an RV through California in May 2019. We visited many places, like Los Angeles, Joshua Tree National Park, Palm Springs, Sequoia and King's Canyon National Park, Fresno, Sacramento and San Francisco.
Which image should be used as background for the header? (default: "")
> usa-170.jpg
```

3. Modify the HTML template under `templates/index_template.jinja` to define the 3 sections:
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

4. Modify the `gallery.json` file to adjust the offset of the background image from 30% to 20%:
```
"background_photo_offset": 20
```

5. Build the gallery - execute the following command:

```
gallery-build
```

