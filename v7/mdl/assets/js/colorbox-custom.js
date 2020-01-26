if (typeof jQuery !== 'undefined') {
    jQuery(function($) {
        $(document).ready(function () {
            $('.thumbnails a').colorbox({
                rel: "gal",
                maxWidth: "100%",
                maxHeight: "100%",
                scalePhotos: true
            });
      	});
  	});
}
