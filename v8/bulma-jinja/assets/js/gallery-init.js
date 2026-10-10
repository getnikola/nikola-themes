// Reads the photo list that gallery.tmpl embeds as a JSON data block.
var galleryData = document.getElementById('gallery-data');
var jsonContent = JSON.parse(galleryData.textContent);
var thumbnailSize = parseInt(galleryData.dataset.thumbnailSize, 10);
renderGallery(jsonContent, thumbnailSize);
window.addEventListener('resize', function(){renderGallery(jsonContent, thumbnailSize)});
