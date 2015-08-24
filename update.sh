#!/bin/sh
workon nikola
git submodule foreach git pull origin master
./scripts/build_themes.py
./scripts/gen_site.py
./scripts/build_site.py
rsync -rav output/code.css output/index.html output/jPages.min.js output/resources output/stmd.js output/theme_data.js output/v7 getnikola@direct.ralsina.me:/srv/www/themes.getnikola.com:80
