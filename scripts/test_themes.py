#!/usr/bin/env python

"""Make sanity checks on the provided themes."""

from __future__ import unicode_literals, print_function
import glob

import colorama

from nikola import utils

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return [theme.split('/')[-1] for theme in glob.glob("themes/*")]

def sanity_check(theme=None):
    if theme is None:  # Check them all
        for theme in theme_list():
            sanity_check(theme)
        return
    themes = utils.get_theme_chain(theme)
    if themes[-1] != 'base':
        error("theme {0} doesn't inherit from base".format(theme))


if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(sanity_check)
