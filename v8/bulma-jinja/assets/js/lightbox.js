// Starts the baguetteBox lightbox; base_helper.tmpl loads this only on pages
// with image-reference links. Deferred to DOMContentLoaded so it also sees the
// links that a gallery page renders from its photo list.
document.addEventListener('DOMContentLoaded', () => {
    baguetteBox.run('div#content', {
        ignoreClass: 'islink',
        captions: function(element){var i=element.getElementsByTagName('img')[0];return i===undefined?'':i.alt;}});
});
