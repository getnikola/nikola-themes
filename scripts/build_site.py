#!/usr/bin/env python

"""Inspect themes, create a JSON describing all the data."""

from __future__ import unicode_literals, print_function
import codecs
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
    data['chain'] = utils.get_theme_chain(theme)
    data['name'] = theme
    readme = utils.get_asset_path('README.md', data['chain'])
    conf_sample = utils.get_asset_path('conf.py.sample', data['chain'])
    if readme:
        data['readme'] = codecs.open(readme, 'r', 'utf8').read()
    else:
        data['readme'] = 'No readme file available'
    if conf_sample:
        data['readme'] += '\n\n**Suggested Configuration:**\n```\n{0}\n```\n\n'.format(codecs.open(conf_sample, 'r', 'utf8').read())

    data['bootswatch'] = ('bootstrap' in data['chain'] or
        'bootstrap-jinja' in data['chain'] or
        'bootstrap3-jinja' in data['chain'] or
        'bootstrap3' in data['chain']) and \
        'bootstrap3-gradients' not in data['chain']
    data['engine'] = utils.get_template_engine(data['chain'])
    data['chain'] = data['chain'][::-1]
    return data

if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(build_site)
