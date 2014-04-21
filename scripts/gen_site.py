#!/usr/bin/env python

import codecs
import glob
import json
import os

import colorama

from nikola import utils

def create_site():
    for theme in glob.glob(os.path.join('themes', '*')):

        read_theme(theme)

def read_theme(theme):
    # Gather this theme's data
    theme_name = os.path.basename(theme)
    data = {}
    data['name'] = theme_name
    readme = os.path.join(theme, 'README.md')
    if os.path.isfile(readme):
        with codecs.open(readme, 'r', 'utf8') as inf:
            data['readme'] = inf.read()
    else:
        data['readme'] = ''

    themes = utils.get_theme_chain(theme_name)
    data['engine'] = utils.get_template_engine(themes)


    if 'bootstrap3' in themes:
        data['bs_version'] = 3
    elif 'bootstrap' in themes:
        data['bs_version'] = 2
    else:
        data['bs_version'] = 0

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

if __name__ == "__main__":
    colorama.init()
    create_site()
