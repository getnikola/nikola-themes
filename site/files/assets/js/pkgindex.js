// Helper JS for Nikola PkgIndex (side menu)

$(document).ready(function() {
    $('#sidemenu-container').load("/sidemenu.html #sidemenu", complete=function() {
        $(".sidemenu-item").filter('[data-name="' + pkgindex_item_name + '"]').addClass('active');
    });
});
