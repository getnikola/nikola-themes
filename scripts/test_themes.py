#!/usr/bin/env python

"""Make sanity checks on the provided themes."""

from __future__ import unicode_literals, print_function
import filecmp
import glob
import hashlib
import os

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
    engine = utils.get_template_engine(themes)

    # Inheritance checks

    # All themes must inherit from base
    if themes[-1] != 'base':
        error("theme {0} doesn't inherit from base".format(theme))
    # All jinja themes must inherit from base-jinja
    if engine == "jinja" and "base-jinja" not in themes:
        error("theme {0} is jinja-based and doesn't inherit from base-jinja".format(theme))
    # All mako themes must NOT inherit from base-jinja
    if engine == "mako" and "base-jinja" in themes:
        error("theme {0} is mako-based and inherits from base-jinja".format(theme))

    # Detect exact asset duplication in theme chain
    for root, dirs, files in os.walk("themes/"+theme):
        for f in files:
            path = "/".join([root, f])
            asset = path.split("/",2)[-1]
            r, p1, p2 = is_asset_duplicated(asset, themes)
            if r:
                error("duplicated asset: {0} {1}".format(p1, p2))

def is_asset_duplicated(path, themes):
    # First get the path for the asset with whole theme chain
    p1 = utils.get_asset_path(path, themes)
    # Get the path for asset with truncated theme chain
    p2 = utils.get_asset_path(path, themes[1:])
    # Compare
    if p1 and p2:
        return filecmp.cmp(p1, p2, False), p1, p2
    else:
        return False, p1, p2

if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(sanity_check)
