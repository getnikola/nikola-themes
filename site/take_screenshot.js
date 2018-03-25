const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

// Simple error checking
var arg_count = process.argv.length - 1;
if (arg_count < 4 || arg_count > 5) {
    console.log('Usage: take_screenshot.js HTML_FILE WIDTH HEIGHT IMAGE_PATH');
    process.exit(1);
}

var executablePath = '';

var pathsToTest = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-dev',
    '/usr/bin/chromium'
];
var pathFound = false;

for (var i = 0; i < pathsToTest.length; i++) {
    var executablePath = pathsToTest[i];
    if (fs.existsSync(executablePath)) {
        pathFound = true;
        break;
    }
}

if (!pathFound) {
    console.log('Chrome(ium) not found. Please add it to take-screenshot.js.');
    process.exit(1);
}

(async () => {
    const browser = await puppeteer.launch({executablePath: executablePath});
    const page = await browser.newPage();

    await page.goto('file://' + path.resolve(process.argv[2]));
    await page.setViewport({width: parseInt(process.argv[3]), height: parseInt(process.argv[4])});
    await page.screenshot({path: process.argv[5], type: 'png', fullPage: true});

    await browser.close();
})();
