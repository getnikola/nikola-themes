#!/bin/sh
git submodule update --init
git submodule foreach git pull origin master
cd site
nikola build
rsync -rav output/ getnikola@direct.ralsina.me:/srv/www/themes.getnikola.com:80
