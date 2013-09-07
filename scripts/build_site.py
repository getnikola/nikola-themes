#!/usr/bin/env python

"""Inspect themes, create a JSON describing all the data."""

from __future__ import unicode_literals, print_function
import glob

import colorama
from progressbar import ProgressBar

from nikola import utils

BASE_URL = "http://themes.nikola.ralsina.com.ar/v6/"

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return ['base', 'bootstrap', 'bootstrap3'] + [theme.split('/')[-1] for theme in glob.glob("themes/*")]

def build_site():
        progress = ProgressBar()
        for theme in progress(theme_list()):
            print(theme)
        return

if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(build_site)
