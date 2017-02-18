var fs = require('fs');
var page = require('webpage').create();
var system = require('system');

// Simple error checking
var arg_count = system.args.length - 1;
if (arg_count < 4 || arg_count > 5) {
    console.log('Usage: take_screenshot.js HTML_FILE WIDTH HEIGHT IMAGE_PATH');
    phantom.exit(1);
}

// Extract arguments
var source_path = system.args[1];
var window_width = system.args[2];
var window_height = system.args[3];
var destination_image_path = system.args[4];

var fullpath = fs.workingDirectory + fs.separator + source_path;
console.log('Screenshot source: ' + fullpath);

// Screen dimensions
page.viewportSize = {
    width: window_width,
    height: window_height
};

// Open page
page.open(fullpath, function() {
    //////////////////////
    // To prevent some pages from being transparent
    // ref: https://uggedal.com/journal/phantomjs-default-background-color/
    page.evaluate(function() {
        var style = document.createElement('style');
        var text = document.createTextNode('body { background: #fff }');
        style.setAttribute('type', 'text/css');
        style.appendChild(text);
        document.head.insertBefore(style, document.head.firstChild);
    });
    //////////////////////

    // Take the screenshot
    // ref: http://phantomjs.org/api/webpage/method/render.html
    page.render(destination_image_path, {});
    phantom.exit(0);
});

