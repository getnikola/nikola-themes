#!/usr/bin/env python

"""Inspect themes, create a JSON describing all the data."""

from __future__ import unicode_literals, print_function
import io
import glob
import json
import os

import colorama

from nikola import utils

import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

MINIMUM_VERSION_SUPPORTED = 6
MAXIMUM_VERSION_SUPPORTED = 7
ALL_VERSIONS_SUPPORTED = list(range(MINIMUM_VERSION_SUPPORTED, MAXIMUM_VERSION_SUPPORTED + 1))

MINIMUM_VERSION_DISPLAYED = 7
MAXIMUM_VERSION_DISPLAYED = 7
ALL_VERSIONS_DISPLAYED = list(range(MINIMUM_VERSION_DISPLAYED, MAXIMUM_VERSION_DISPLAYED + 1))

GLOB = "v{0}/*".format(MAXIMUM_VERSION_SUPPORTED)
DIR = "v{0}".format(MAXIMUM_VERSION_SUPPORTED)

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return sorted(['base', 'base-jinja', 'bootstrap3', 'bootstrap3-jinja'] + [theme.split('/')[-1] for theme in glob.glob(GLOB)])

def build_site():
    data = {}
    for theme in theme_list():
        data[theme] = get_data(theme)

    data['__meta__'] = {'allver': ALL_VERSIONS_DISPLAYED}
    with io.open(os.path.join('output', 'theme_data.js'), 'w+', encoding='utf-8') as outf:
        outf.write("var data = " + json.dumps(data, indent=4, ensure_ascii=True, sort_keys=True))

def get_data(theme):
    data = {}
    data['chain'] = utils.get_theme_chain(theme, [DIR, 'themes'])
    data['name'] = theme
    readme = utils.get_asset_path('README.md', data['chain'])
    conf_sample = utils.get_asset_path('conf.py.sample', data['chain'])
    if readme:
        data['readme'] = io.open(readme, 'r', encoding='utf-8').read()
    else:
        data['readme'] = 'No README.md file available.'

    if conf_sample:
        data['confpy'] = pygments.highlight(
            io.open(conf_sample, 'r', encoding='utf-8').read(),
            PythonLexer(), HtmlFormatter(cssclass='code'))
    else:
        data['confpy'] = None

    data['bootswatch'] = ('bootstrap' in data['chain'] or
        'bootstrap-jinja' in data['chain'] or
        'bootstrap3-jinja' in data['chain'] or
        'bootstrap3' in data['chain']) and \
        'bootstrap3-gradients' not in data['chain']
    data['engine'] = utils.get_template_engine(data['chain'])
    data['chain'] = data['chain'][::-1]

    data['allver'] = []
    for v in ALL_VERSIONS_SUPPORTED:
        if glob.glob('v{0}/*'.format(v)):
            data['allver'].append(v)

    return data

if __name__ == "__main__":
    colorama.init()
    print("Building theme_data.js")
    build_site()
