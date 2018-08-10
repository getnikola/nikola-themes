$(document).ready(function() {
    $("select.navbar-dropdown").change(function() {
        window.location = $(this).find("option:selected").val();
    });
});
