var slides = {}

function createSlides() {
  $("a.gallery-photo").each(function (photo_id, photo) {
    var slide = {
      w:    photo.getAttribute('data-width'),
      h:    photo.getAttribute('data-height'),
      msrc: photo.getElementsByTagName('img')[0].getAttribute('src'),
      title: photo.getElementsByTagName('img')[0].getAttribute('alt'),
    };

    if (photo.getAttribute('data-type') == 'image')
      slide['src'] = photo.getAttribute('href');
    else
      slide['html'] = '<video style="margin: 0px auto; height: 100%; max-width: 100%; max-height: 100%;" data-index="' + photo.getAttribute('data-index') +
                      '" controls><source src="' + photo.getAttribute('href') + '" type="video/mp4"></video>';

    var gallery_id = parseInt(photo.getAttribute('data-gallery'));
    if (!(gallery_id in slides))
      slides[gallery_id] = [];

    slides[gallery_id].push(slide);
  });
}

function getThumbBounds(gallery, index) {
  var thumbnail = $('div.gallery a[data-gallery="'+gallery+'"][data-index="'+index+'"]')[0];
  var pageYScroll = window.pageYOffset || document.documentElement.scrollTop;
  var rect = thumbnail.getBoundingClientRect();
  return {x: rect.left, y: rect.top + pageYScroll, w: rect.width};
}

function openPhotoSwipe() {
  var index = parseInt($(this).attr('data-index'))
  var gallery_id = $(this).attr('data-gallery')

  var options = {
    index: index,
    getThumbBoundsFn: function (id) { return getThumbBounds(gallery_id, id) },
    preload: [2,5],
    zoomEl: false,
    shareEl: true,
    barsSize: {top:0, bottom:0},
    bgOpacity: 1,
    loop: false,
    mainClass: 'pswp--minimal--dark',
    shareButtons: [
        {id:'download', label:'Download image', url:'{{raw_image_url}}', download:true}
    ],
  };

  var gallery = new PhotoSwipe( $('.pswp')[0], PhotoSwipeUI_Default, slides[gallery_id], options);

  gallery.listen('afterChange', function() {
    var videos = $('div.pswp__item video')
    for (var i=0; i<videos.length; ++i)
      videos[i].pause()

    if (this.currItem.html) {
      var videos = $('div.pswp__item video[data-index='+this.getCurrentIndex()+']')
      if (videos.length > 0)
        videos[0].play()
    }
  });

  gallery.init();

  return false;
}


$( document ).ready(function() {
  createSlides()
  $('div.gallery a').on('click', openPhotoSwipe)
});
