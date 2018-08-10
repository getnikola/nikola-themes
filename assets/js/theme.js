$(document).ready(function() {

    var $window = $(window),
        $nav = $('.navbar'),
        $footnotes = $('.footnote'),
        $docutilsContainers = $('.docutils.container');

    function init() {
        fixFootnotes();
        fixDocutilContainers();
        $window.on('load hashchange', fixHashOffset);
    }

    function fixFootnotes() {
        $footnotes.each(function(i, el) {
            $el = $(el);
            $el.appendTo($el.closest('.entry-content,.entry-summary'));
        });
    }

    function fixHashOffset() {
        if($window.scrollTop() >= $nav.offset().top) {
            scrollBy(0, -$nav.height());
        }
    }

    function fixDocutilContainers() {
        $docutilsContainers.each(function(i, el) {
            $el = $(el);
            $el.removeClass('container').addClass('du-container')
        });
    }

    init();
});
