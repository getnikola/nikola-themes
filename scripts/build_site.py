#!/usr/bin/env python

"""Inspect themes, create a JSON describing all the data."""

from __future__ import unicode_literals, print_function
import glob
import json
import os

import colorama
from progressbar import ProgressBar

from nikola import utils

BASE_URL = "http://themes.nikola.ralsina.com.ar/v6/"

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return ['base', 'bootstrap', 'bootstrap3'] + [theme.split('/')[-1] for theme in glob.glob("themes/*")]

def build_site():
    data = {}
    progress = ProgressBar()
    for theme in progress(theme_list()):
        data[theme] = get_data(theme)
    with open(os.path.join('output', 'v6', 'theme_data.js'), 'wb+') as outf:
        outf.write("var data = " + json.dumps(data, indent=4, ensure_ascii=True, sort_keys=True))

def get_data(theme):
    data = {}
    data['name'] = theme
    readme = os.path.join("themes", theme, "README")
    if os.path.isfile(readme):
        data['readme'] = open(readme).read()
    else:
        data['readme'] = 'No readme file available'
    data['chain'] = utils.get_theme_chain(theme)
    data['bootswatch'] = ('bootstrap' in data['chain'] or
        'bootstrap-jinja' in data['chain'] or
        'bootstrap3-jinja' in data['chain'] or
        'bootstrap3' in data['chain']) and \
        'bootstrap3-gradients' not in data['chain']
    data['engine'] = utils.get_template_engine(data['chain'])
    return data

if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(build_site)
